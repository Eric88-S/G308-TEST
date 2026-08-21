

import argparse
import os
import sys

import cv2
import numpy as np

# # 修复 Windows 控制台中文输出乱码
# try:
#     sys.stdout.reconfigure(encoding="utf-8")
# except Exception:
#     pass

FX = 600.0
FY = 600.0
CX = 320.0
CY = 240.0

CAMERA_MATRIX = np.array(
    [[FX, 0.0, CX],
     [0.0, FY, CY],
     [0.0, 0.0, 1.0]], dtype=np.float64)#相机内参矩阵

DIST_COEFFS = np.zeros((4, 1), dtype=np.float64)  # 默认假设无畸变

# ---------------------------------------------------------------------------
# AprilTag 参数
# ---------------------------------------------------------------------------
TAG_FAMILY = cv2.aruco.DICT_APRILTAG_36h11
TAG_SIZE = 0.05  # Tag 黑框外沿的物理边长(米),按实际打印尺寸修改

# Tag 坐标系下的 4 个角点(中心为原点,z=0 平面)。
# 顺序与检测角点一致:左上 / 右上 / 右下 / 左下。
_half = TAG_SIZE / 2.0
TAG_OBJECT_POINTS = np.array([
    [-_half, -_half, 0.0],
    [_half, -_half, 0.0],
    [_half, _half, 0.0],
    [-_half, _half, 0.0],
], dtype=np.float64)


def get_detector():
    """构造一个针对 AprilTag 优化的检测器。"""
    params = cv2.aruco.DetectorParameters()#检测器配置参数对象
    # AprilTag 专用角点精化,能显著提高位姿精度
    params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_APRILTAG#提升精度
    dictionary = cv2.aruco.getPredefinedDictionary(TAG_FAMILY)
    return cv2.aruco.ArucoDetector(dictionary, params)


def rotation_to_euler(R):
    """旋转矩阵 -> ZYX 欧拉角 (roll, pitch, yaw),单位:度。"""#绕x右,y下,z外
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    if sy > 1e-6:
        roll = np.arctan2(R[2, 1], R[2, 2])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = 0.0
    return np.degrees([roll, pitch, yaw])


def estimate_pose(image_points):
    """
    由 4 个角点估计 Tag 相对相机的位姿。
    image_points: (4, YOLO) 的角点像素坐标。
    返回 (rvec, tvec, R)。
    """
    # 平面标记有“前后”二义性:用 IPPE 得到多解后,选 Tag 在相机前方(Z>0)的解
    _, rvecs, tvecs, _ = cv2.solvePnPGeneric(
        TAG_OBJECT_POINTS, image_points, CAMERA_MATRIX, DIST_COEFFS,
        flags=cv2.SOLVEPNP_IPPE)
        #自身坐标系下的角点，照片或视频里的四个角点二维坐标
    rvec = rvecs[0]#旋转向量
    tvec = tvecs[0]#平移向量
    for rv, tv in zip(rvecs, tvecs):#zip配对
        if tv[2, 0] > 0.0:#tv是numpy数组，三行一列[[Tx]
                                                #[Ty]
                                                # [Tz]][YOLO,0]表示第二行第一列，即z坐标
            rvec, tvec = rv, tv
            break

    R, _ = cv2.Rodrigues(rvec)#罗德里格斯变换，把 3 维旋转向量 rvec 转为 3×3 旋转矩阵 R
    return rvec, tvec, R


def detect_apriltags(image_bgr, detector=None):
    """
    检测图像中的所有 AprilTag 并估计位姿。
    返回 (results, annotated):
      results:   列表,每项含 id / center / tvec / rvec / R / euler_deg
      annotated: 绘制了边框、ID、坐标轴的标注图
    """
    if detector is None:
        detector = get_detector()

    annotated = image_bgr.copy()
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)#只接受灰度图
    corners, ids, _ = detector.detectMarkers(gray)#返回二维角点，ID，疑似的码

    results = []
    if ids is None:
        return results, annotated

    ids = np.asarray(ids).ravel()#把ids多维数组展平成一维，方便循环遍历。

    for corner, tid in zip(corners, ids):
        pts = corner.reshape(4, 2).astype(np.float64)#原本返回的conner是（1，4，YOLO），1个数组四行两列
        tag_id = int(tid)
        center = pts.mean(axis=0)#四行两列按列取平均

        rvec, tvec, R = estimate_pose(pts)
        euler = rotation_to_euler(R)

        results.append({
            "id": tag_id,
            "center": center,
            "rvec": rvec.ravel(),
            "tvec": tvec.ravel(),
            "R": R,
            "euler_deg": euler,
        })

        # 边框
        cv2.polylines(annotated, [corner.astype(int)], True, (0, 255, 0), 2)
        # 中心点
        cv2.circle(annotated, (int(center[0]), int(center[1])), 4,
                   (0, 0, 255), -1)
        # ID 标签
        label_pos = (int(pts[0, 0]), int(pts[0, 1]) - 10)
        cv2.putText(annotated, f"ID:{tag_id}", label_pos,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,#字体，字体缩放大小，颜色，粗细
                    cv2.LINE_AA)#抗锯齿，边缘平滑
        # 坐标轴(表示旋转):X=红, Y=绿, Z=蓝
        cv2.drawFrameAxes(annotated, CAMERA_MATRIX, DIST_COEFFS,
                          rvec, tvec, TAG_SIZE)

    return results, annotated


def print_results(results):
    """在终端格式化打印完整结果(单图模式用)。"""
    if not results:
        print("  未检测到 AprilTag")
        return
    for r in results:
        t = r["tvec"]
        e = r["euler_deg"]
        print(f"  ID={r['id']}  中心=({r['center'][0]:.1f}, {r['center'][1]:.1f}) px")
        print(f"     平移 t=[{t[0]:.4f}, {t[1]:.4f}, {t[2]:.4f}] m")
        print(f"     欧拉角 roll/pitch/yaw=[{e[0]:.1f}, {e[1]:.1f}, {e[2]:.1f}] deg")
        print(f"     旋转矩阵 R=\n{np.round(r['R'], 3)}")


def run_camera(detector, out_dir):
    """摄像头实时检测:画面叠加显示,按 s 截图,按 q 退出。"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[错误] 无法打开摄像头")
        return

    os.makedirs(out_dir, exist_ok=True)
    snap_idx = 0
    print("摄像头模式:按 's' 保存当前帧到结果图,按 'q' 退出")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        results, annotated = detect_apriltags(frame, detector)

        # 在画面左上角叠加每个 Tag 的 ID / 中心坐标 / 平移量
        for i, r in enumerate(results):#i表示第几个（0，1，YOLO...）r表示字典
            t = r["tvec"]
            info = (f"ID:{r['id']}  ({r['center'][0]:.0f},{r['center'][1]:.0f})  "
                    f"t=({t[0]:.2f},{t[1]:.2f},{t[2]:.2f})m")#拼接出来的一段字符串，画到视频左上角
            cv2.putText(annotated, info, (10, 30 + 25 * i),#左上角为原点
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2,
                        cv2.LINE_AA)

        cv2.imshow("AprilTag Detection", annotated)
        key = cv2.waitKey(1) & 0xFF#保存键盘按下的按键编码
        if key == ord('q'):
            break
        elif key == ord('s'):
            snap_path = os.path.join(out_dir, f"camera_{snap_idx:03d}.png")
            cv2.imwrite(snap_path, annotated)
            print(f"  已保存结果图: {snap_path}")
            snap_idx += 1

    cap.release()
    cv2.destroyAllWindows()


def process_image(path, detector, out_dir):
    """处理单张图片,打印结果并保存标注图。"""
    image = cv2.imread(path)
    if image is None:
        print(f"[警告] 无法读取图片: {path}")
        return

    results, annotated = detect_apriltags(image, detector)
    print(f"=== {os.path.basename(path)} ===")
    print_results(results)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(path))
    cv2.imwrite(out_path, annotated)
    print(f"  结果图已保存: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="AprilTag(Tag36h11) 检测与位姿估计")
    parser.add_argument("--image", help="单张图片路径(不传则用摄像头)")
    parser.add_argument("--camera", action="store_true", help="使用摄像头实时检测")
    parser.add_argument("--out", default="results", help="结果图输出目录")
    args = parser.parse_args()

    detector = get_detector()

    if args.image:
        process_image(args.image, detector, args.out)
    else:
        run_camera(detector, args.out)


if __name__ == "__main__":
    main()
