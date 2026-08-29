"""
recognition_node.py — 设备B

五步流水线（见 process_callback）：
  ① 摄像头取流  ② Canny 边缘检测定位屏幕  ③ 屏幕内识别算式
  ④ SymPy 计算  ⑤ 发布到 /calculation_result

识别为什么不用 Tesseract：实测它在完全无降质的原图上也 100% 把 ÷ 读成 +
（132÷3 → 132+3），而结果仍是合法算式，会静默发布错误答案。
本场景字符固定为 0-9 和 + - × ÷ 共 14 个、字体固定 Times New Roman，
因此启动时用显示端同一个 TTF 渲染模板，逐字做相似度匹配。
"""

import os
import re
import signal
import threading

import cv2
import numpy as np
import rclpy
from PIL import Image, ImageDraw, ImageFont
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sympy import N, simplify

from calculation_interfaces.msg import CalculationResult

CHARS = '0123456789+-×÷'
SIZE = 32                                        # 字符归一化边长
EXPR_RE = re.compile(r'^\d+([+\-×÷]\d+)+$')      # 合法算式：数字(运算符数字)+


def _norm(mask):
    """裁到笔画外接框 → 补成正方形 → 缩放到 SIZE×SIZE。

    补正方形而不是直接拉伸，是为了保留宽高比：否则 '-' 拉伸后和 '1' 一模一样。
    """
    ys, xs = np.where(mask > 0)#选出数字
    if len(ys) == 0:
        return np.zeros((SIZE, SIZE), np.float32)
    c = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]#组成数组
    h, w = c.shape
    s = max(h, w)
    sq = np.zeros((s, s), np.uint8)
    sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = c
    return cv2.resize(sq, (SIZE, SIZE), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


def build_templates(font_path):
    """用显示端同一个 Times New Roman 渲染 14 个字符模板（已单位化，匹配时点乘即可）"""
    font = ImageFont.truetype(font_path, 150)#加载真实字体
    templates = {}
    for ch in CHARS:
        img = Image.new('L', (300, 300), 255)#新建空白图片，L表示单通道灰度图，size，color
        draw = ImageDraw.Draw(img)#建立画笔变量，之后可以画图
        b = draw.textbbox((0, 0), ch, font=font)#计算出文字在图上占用的盒型大小，不画图，返回（left，top，right，bottom）
        draw.text(((300 - (b[2] - b[0])) // 2 - b[0],
                   (300 - (b[3] - b[1])) // 2 - b[1]), ch, font=font, fill=0)
        t = _norm((np.array(img) < 128).astype(np.uint8) * 255)#img灰度图不一定是二值图，按128分类false和ture，通过astype转化为0,1再乘255
        templates[ch] = t / (np.linalg.norm(t) + 1e-9)#np.linalg.norm看成长一维向量算模长，加1e-9防止分母为0,设立一个标准，方便后面字符比对，算一个单位向量，后面的图片除以单位向量得到cos值，为1则置信度高
    return templates


def segment(ink):
    """从二值图（白字黑底）切出每个字符的外接框，从左到右排序。

    三条规则：
      1. 贴边的连通域是屏幕边框，丢掉（算式总是居中显示、四周有留白）
      2. 只保留最高分量所在的那一行，排除反光点
      3. '÷' 由上点+横线+下点三个连通域组成，按 x 区间重叠合并回一个字符
    """
    _, _, stats, _ = cv2.connectedComponentsWithStats(ink, 8)#找到图片上所有白色连通区域（字符），返回：连通域总数，每个像素属于第几连通域，连通域信息（x，Y：包围盒左上角，w，h：宽高，area：像素面积），每个区域中心点
    H, W = ink.shape
    boxes = [[x, y, w, h] for x, y, w, h, a in stats[1:]#stats[0]专门存储背景
             if a >= 5 and x > 1 and y > 1 and x + w < W - 1 and y + h < H - 1]
    if not boxes:
        return []

    ref = max(boxes, key=lambda b: b[3])#lambda是一种快速写临时匿名小函数，lambda输入：输出
    top, bottom = ref[1] - 0.6 * ref[3], ref[1] + 1.6 * ref[3]
    boxes = [b for b in boxes
             if top <= b[1] + b[3] / 2 <= bottom and b[3] <= 1.6 * ref[3]]
    boxes.sort(key=lambda b: b[0])

    merged = []
    for x, y, w, h in boxes:
        if merged:
            px, py, pw, ph = merged[-1]
            if min(px + pw, x + w) - max(px, x) > 0.55 * min(pw, w):
                nx, ny = min(px, x), min(py, y)
                merged[-1] = [nx, ny, max(px + pw, x + w) - nx, max(py + ph, y + h) - ny]
                continue
        merged.append([x, y, w, h])
    return merged


class RecognitionNode(Node):

    def __init__(self):
        super().__init__('recognition_node')

        self.declare_parameter('camera_device', 0)
        self.declare_parameter('frame_width', 1280)
        self.declare_parameter('frame_height', 720)
        self.declare_parameter('preview', True)
        self.declare_parameter('process_rate', 2.0)
        self.declare_parameter(
            'font_path', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf')

        self.preview = self.get_parameter('preview').value
        self.templates = build_templates(self.get_parameter('font_path').value)

        self.pub = self.create_publisher(CalculationResult, '/calculation_result', 10)

        # ---- ① 摄像头取流 ----
        device = self.get_parameter('camera_device').value
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.get_parameter('frame_width').value)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.get_parameter('frame_height').value)
        if not self.cap.isOpened():
            raise RuntimeError(f'摄像头 /dev/video{device} 打开失败')

        self._lock = threading.Lock()
        self._running = True
        self.frame = None
        self.screen_rect = None
        self.text = ''
        self.last_published = ''

        threading.Thread(target=self._capture_loop, daemon=True).start()
        rate = self.get_parameter('process_rate').value
        self.create_timer(1.0 / rate, self.process_callback)
        self.get_logger().info(f'识别节点启动（{rate}Hz）')

    # ---- ① 采集线程：满速读帧 + 预览 ----
    def _capture_loop(self):
        while self._running:
            ok, frame = self.cap.read()
            if not ok:
                continue
            with self._lock:
                self.frame = frame.copy()
                rect, text = self.screen_rect, self.text

            if not self.preview:
                continue
            if rect is not None:
                x, y, w, h = rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # putText 只支持 ASCII，× ÷ 是 UTF-8 双字节，会显示成 ??。
            # 仅预览时换成 x 和 /，发布到话题的算式仍保持 × ÷ 原样。
            preview_text = (text or 'searching...').replace('×', 'x').replace('÷', '/')
            cv2.putText(frame, preview_text, (20, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2)
            cv2.imshow('Recognition (q to quit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._running = False
                os.kill(os.getpid(), signal.SIGINT)   # 子线程 raise 传不到主线程
                return

    # ---- ② Canny 边缘检测定位屏幕 ----
    def find_screen(self, gray):
        edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
        edges = cv2.dilate(edges, np.ones((5, 5), np.uint8))   # 连上断裂的屏幕边框
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) < 0.02 * gray.size:            # 太小，不是屏幕
            return None
        return cv2.boundingRect(cnt)

    # ---- ③ 屏幕内识别算式 ----
    def read_expression(self, screen):
        """白底黑字用 Otsu 全局阈值。

        二值化前先升采样 + 反锐化：远距离拍摄时 '÷' 的两点和 '+' 的竖笔只剩一两个
        像素，直接硬阈值会把它们抹掉、双双塌缩成 '-'。这步把远距离识别率 3/6 拉到 6/6。
        """
        scale = min(4.0, max(1.0, 300.0 / screen.shape[0]))
        if scale > 1.05:
            screen = cv2.resize(screen, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        sharp = cv2.addWeighted(screen, 1.8, cv2.GaussianBlur(screen, (0, 0), 2), -0.8, 0)
        _, ink = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        chars = []
        for x, y, w, h in segment(ink):
            v = _norm(ink[y:y + h, x:x + w])
            if v.sum() > 1e-6:
                chars.append(max(CHARS, key=lambda c: float(np.sum(v * self.templates[c]))))
        return ''.join(chars)

    # ---- 主流程 ----
    def process_callback(self):
        with self._lock:
            frame = self.frame.copy() if self.frame is not None else None
        if frame is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rect = self.find_screen(gray)                          # ②
        with self._lock:
            self.screen_rect = rect
        if rect is None:
            return

        x, y, w, h = rect
        expression = self.read_expression(gray[y:y + h, x:x + w])   # ③
        if not EXPR_RE.match(expression):
            return

        try:                                                    # ④
            result = float(N(simplify(expression.replace('×', '*').replace('÷', '/'))))
        except Exception as exc:
            self.get_logger().warn(f'计算失败 "{expression}": {exc}')
            return

        with self._lock:
            self.text = f'{expression} = {result:g}'

        if expression != self.last_published:                    # ⑤
            msg = CalculationResult()
            msg.raw_expression = expression
            msg.result = result
            self.pub.publish(msg)
            self.last_published = expression
            self.get_logger().info(f'>>> 发布: "{expression}" = {result:g}')

    def destroy_node(self):
        self._running = False
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RecognitionNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        executor.shutdown()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
