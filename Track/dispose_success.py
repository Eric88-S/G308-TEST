import cv2
import numpy as np

image = cv2.imread('saidao.jpeg')
image_copy = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_yellow = np.array([15, 100, 100])
upper_yellow = np.array([20, 255, 255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

kernel = np.ones((5, 5), np.uint8)
mask_closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

h, w = mask_closing.shape
center_pts = []
right_pts = []
left_pts = []
for y in range(h):
    xs = np.where(mask_closing[y] > 0)[0]   # np.where表示所有ture的下标值
    if len(xs) >= 2:
          left = xs[0]                         # 最左黄线
          right = xs[-1]                       # 最右黄线
          center_pts.append(((left + right) // 2, y))
          left_pts.append((left,y))
          right_pts.append((right,y))

    if center_pts:
      c_pts = np.array(center_pts, dtype=np.int32)
      l_pts = np.array(left_pts, dtype=np.int32)
      r_pts = np.array(right_pts, dtype=np.int32)
      cv2.polylines(image_copy, [c_pts], False, (0, 0, 255), 2)  # 红色中线
      cv2.polylines(image_copy, [l_pts], False, (0, 255,0), 2)
      cv2.polylines(image_copy, [r_pts], False, (0, 255,0), 2)

cv2.imshow('image', image)
cv2.imshow('image_copy', image_copy)
cv2.imshow('mask_closing', mask_closing)
cv2.waitKey(0)
cv2.destroyAllWindows()

