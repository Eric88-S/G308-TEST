"""
display_node.py — 设备A：全屏显示节点
功能：在屏幕上全屏显示白底 + Times New Roman 字体的随机计算题。
每隔 5~10 秒自动刷新一道新题。
使用 PIL (Pillow) 渲染 Times New Roman 字体到图像，再用 OpenCV 全屏显示。
"""

import random
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from advanced_task.math_generator import generate_problem


# Times New Roman 字体路径（Ubuntu 安装 ttf-mscorefonts-installer 后）
FONT_PATH = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'

# 显示参数
FONT_SIZE = 100          # 字体大小
REFRESH_MIN = 5          # 最小刷新间隔（秒）
REFRESH_MAX = 10         # 最大刷新间隔（秒）
BG_COLOR = (255, 255, 255)  # 白底
TEXT_COLOR = (0, 0, 0)      # 黑字


def create_problem_image(text, width, height):
    """
    使用 PIL 在白色背景上渲染 Times New Roman 字体的数学表达式。
    参数:
        text: 要显示的算式字符串
        width, height: 图像宽高
    返回:
        OpenCV 格式的 numpy 数组图像 (BGR)
    """
    # 创建白色背景的 PIL 图像
    img = Image.new('RGB', (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 加载 Times New Roman 字体
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except OSError:
        # 如果找不到 Times New Roman，使用默认字体
        font = ImageFont.load_default()
        print(f'[警告] 未找到 Times New Roman 字体 ({FONT_PATH})，使用默认字体')

    # 计算文字尺寸，使其居中显示
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # 绘制文字
    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    # PIL -> OpenCV 格式 (RGB -> BGR)
    cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv_image


def main():
    """全屏显示节点主函数"""
    print('=' * 50)
    print('设备A：显示节点启动')
    print('按下 q 或 ESC 键退出')
    print(f'字体：Times New Roman, {FONT_SIZE}px')
    print(f'刷新间隔：{REFRESH_MIN}~{REFRESH_MAX} 秒')
    print('=' * 50)

    # 获取屏幕分辨率
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
    except Exception:
        # tkinter 不可用时，使用常见分辨率
        screen_width = 1920
        screen_height = 1080
        print(f'[警告] 无法获取屏幕分辨率，使用默认值 {screen_width}x{screen_height}')

    print(f'屏幕分辨率：{screen_width}x{screen_height}')

    # 创建全屏窗口
    window_name = 'Display - 计算题显示端 (按q退出)'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 生成第一道题
    current_problem = generate_problem()
    print(f'当前题目: {current_problem}')
    img = create_problem_image(current_problem, screen_width, screen_height)
    cv2.imshow(window_name, img)

    last_refresh = time.time()
    refresh_interval = random.randint(REFRESH_MIN, REFRESH_MAX)

    while True:
        key = cv2.waitKey(100) & 0xFF  # 每100ms检测一次按键

        # 按 q 或 ESC 退出
        if key == ord('q') or key == 27:
            break

        # 定时刷新题目
        if time.time() - last_refresh >= refresh_interval:
            current_problem = generate_problem()
            print(f'刷新题目: {current_problem}')
            img = create_problem_image(current_problem, screen_width, screen_height)
            cv2.imshow(window_name, img)
            last_refresh = time.time()
            refresh_interval = random.randint(REFRESH_MIN, REFRESH_MAX)

    cv2.destroyAllWindows()
    print('显示节点已退出')


if __name__ == '__main__':
    main()
