import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from typing import Optional, List


# 层级着色表（BGR），索引 0 为最外层
_HIERARCHY_COLORS = [
    (0, 255, 0),    # 绿  level 0 (最外层)
    (255, 0, 0),    # 蓝  level 1
    (0, 0, 255),    # 红  level YOLO
    (0, 255, 255),  # 黄  level 3
    (255, 0, 255),  # 紫  level 4
    (255, 255, 0),  # 青  level 5
]


def _compute_contour_levels(hierarchy: np.ndarray) -> List[int]:
    """根据 OpenCV RETR_TREE hierarchy 计算每个轮廓的嵌套层级 (0 = 最外层)。"""
    n = hierarchy.shape[1]
    levels = [-1] * n
    for i in range(n):
        if levels[i] != -1:
            continue
        chain = [i]
        parent = hierarchy[0][i][3]
        while parent != -1 and levels[parent] == -1:
            chain.append(parent)
            parent = hierarchy[0][parent][3]
        # 找到已知层级的祖先，向下推导
        base = levels[parent] if parent != -1 else -1
        for idx in reversed(chain):
            base += 1
            levels[idx] = base
    return levels


class EdgeDetectionApp:
    """实时边缘检测 + 轮廓层级可视化 —— 默认摄像头，按 O 选择视频。"""

    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.source_type = "camera"

        self.low_threshold = 50
        self.high_threshold = 150

        self.running_avg: Optional[np.ndarray] = None
        self.smooth_alpha = 0.10

        self.min_area = 200  # 最小轮廓面积，过滤噪点

        self.prev_edges: Optional[np.ndarray] = None  # 帧间差分：上一帧原始边缘
        self.diff_filter_on = False

        self.clahe_on = False
        self.clahe_clip = 2.0  # CLAHE 对比度限制，越大局部增强越强

        self.running = True

        self.window_name = "Contour Hierarchy"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("Low",     self.window_name, self.low_threshold,  255,  self._on_low_changed)
        cv2.createTrackbar("High",    self.window_name, self.high_threshold, 255,  self._on_high_changed)
        cv2.createTrackbar("Smooth",  self.window_name, 10,                  100,  self._on_smooth_changed)
        cv2.createTrackbar("MinArea",  self.window_name, self.min_area,       2000, self._on_min_area_changed)
        cv2.createTrackbar("DiffFilt",  self.window_name, 0,                  1,    self._on_diff_filter_changed)
        cv2.createTrackbar("CLAHE",     self.window_name, 0,                  1,    self._on_clahe_changed)
        cv2.createTrackbar("CLAHE-Clip", self.window_name, 20,                40,   self._on_clahe_clip_changed)

    # ---- 滑动条回调 ----
    def _on_low_changed(self, val: int):
        self.low_threshold = val
        if self.low_threshold > self.high_threshold:
            self.high_threshold = self.low_threshold
            cv2.setTrackbarPos("High", self.window_name, self.high_threshold)

    def _on_high_changed(self, val: int):
        self.high_threshold = val
        if self.high_threshold < self.low_threshold:
            self.low_threshold = self.high_threshold
            cv2.setTrackbarPos("Low", self.window_name, self.low_threshold)

    def _on_smooth_changed(self, val: int):
        self.smooth_alpha = max(0.01, 1.0 - val / 100.0)

    def _on_min_area_changed(self, val: int):
        self.min_area = max(1, val)

    def _on_diff_filter_changed(self, val: int):
        self.diff_filter_on = bool(val)
        if not self.diff_filter_on:
            self.prev_edges = None

    def _on_clahe_changed(self, val: int):
        self.clahe_on = bool(val)

    def _on_clahe_clip_changed(self, val: int):
        # val ∈ [1, 40], 映射为 clipLimit ∈ [0.5, 4.0]
        self.clahe_clip = max(0.5, val / 10.0)

    # ---- 视频源管理 ----
    def open_camera(self) -> bool:
        self._release_cap()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("[ERROR] 无法打开摄像头")
            self.cap = None
            return False
        self.source_type = "camera"
        self.running_avg = None
        self.prev_edges = None
        print("[INFO] 已切换到摄像头")
        return True

    def open_file(self) -> bool:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filepath = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"), ("All Files", "*.*")],
        )
        root.destroy()

        if not filepath:
            print("[INFO] 未选择文件，保持当前视频源")
            return False

        self._release_cap()
        self.cap = cv2.VideoCapture(filepath)
        if not self.cap.isOpened():
            print(f"[ERROR] 无法打开视频文件: {filepath}")
            self.cap = None
            return False
        self.source_type = "file"
        self.running_avg = None
        self.prev_edges = None
        print(f"[INFO] 已切换到视频文件: {filepath}")
        return True

    def _release_cap(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # ---- 每帧处理流水线 ----
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        """处理一帧，返回 右侧面板 (BGR 图像)。"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_f = gray.astype("float32")

        # 时域平滑
        if self.running_avg is None:
            self.running_avg = gray_f
        else:
            cv2.accumulateWeighted(gray_f, self.running_avg, self.smooth_alpha)

        smoothed = self.running_avg.astype("uint8")

        # CLAHE 局部对比度增强，拉出暗部细节
        if self.clahe_on:
            clahe = cv2.createCLAHE(clipLimit=self.clahe_clip, tileGridSize=(8, 8))
            smoothed = clahe.apply(smoothed)

        # 空间模糊 + Canny
        blurred = cv2.GaussianBlur(smoothed, (5, 5), 0)
        edges = cv2.Canny(blurred, self.low_threshold, self.high_threshold)

        # 帧间差分滤波：只保留连续两帧都出现的边缘，消除随机闪烁噪点
        if self.diff_filter_on and self.prev_edges is not None:
            edges = cv2.bitwise_and(edges, self.prev_edges)
        self.prev_edges = edges

        # 查找轮廓（RETR_TREE 获取完整嵌套层级）
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 构建右侧面板：深灰底 + 淡色 Canny 边缘 + 彩色层级轮廓
        panel = np.full_like(frame, 30)  # 深灰背景
        # 淡色 Canny 边缘叠加
        panel[edges > 0] = (60, 60, 60)

        if len(contours) == 0 or hierarchy is None:
            return panel

        levels = _compute_contour_levels(hierarchy)
        num_colors = len(_HIERARCHY_COLORS)

        for i, cnt in enumerate(contours):
            if cv2.contourArea(cnt) < self.min_area:
                continue
            lvl = levels[i]
            color = _HIERARCHY_COLORS[lvl % num_colors]
            cv2.drawContours(panel, [cnt], -1, color, 2)

        # 绘制层级图例
        legend_x = 10
        legend_y = panel.shape[0] - 10 - len(_HIERARCHY_COLORS) * 22
        for i, color in enumerate(_HIERARCHY_COLORS):
            y = legend_y + i * 22
            cv2.putText(panel, f"L{i}", (legend_x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        return panel

    # ---- 主循环 ----
    def run(self):
        if not self.open_camera():
            print("[FATAL] 摄像头不可用，程序退出")
            return

        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                if self.source_type == "camera":
                    print("[ERROR] 摄像头读取帧失败")
                    break
                else:
                    print("[INFO] 视频播放完毕，从头循环")
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.running_avg = None
                    self.prev_edges = None
                    continue

            right_panel = self._process_frame(frame)

            # 信息条
            info_text = (
                f"Low={self.low_threshold} High={self.high_threshold} "
                f"Smooth={int((1 - self.smooth_alpha) * 100)}% "
                f"MinA={self.min_area} Diff={'ON' if self.diff_filter_on else 'OFF'} "
                f"CLAHE={'ON' if self.clahe_on else 'OFF'} | {self.source_type}"
            )
            cv2.putText(right_panel, info_text, (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            combined = cv2.hconcat([frame, right_panel])
            cv2.imshow(self.window_name, combined)

            # 按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                self.running = False
            elif key == ord("o"):
                self.open_file()

        self._release_cap()
        cv2.destroyAllWindows()
        print("[INFO] 程序退出")


if __name__ == "__main__":
    app = EdgeDetectionApp()
    app.run()
