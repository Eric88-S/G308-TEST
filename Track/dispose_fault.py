import cv2
import numpy as np

image=cv2.imread('saidao.jpeg')
image_copy=image.copy()
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_yellow = np.array([15, 100, 100])
upper_yellow = np.array([20, 255, 255])

mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
res = cv2.bitwise_and(image, image, mask=mask)

kernel =np.ones((5, 5), np.uint8)
mask_closing=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

edges=cv2.Canny(mask_closing, 50, 150)

#contours,hierarchy=cv2.findContours(mask_closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
h,w=edges.shape
lines=cv2.HoughLinesP(edges,1, np.pi/180, threshold=10,minLineLength=5, maxLineGap=10)
if lines is not None:
    for line in lines:
        x1,y1,x2,y2=line
        if (x1<5 and x2<5) or (x1>w-5 and x2>w-5):
            continue
        if y1<5 and y2<5:
            x3=(x2+x1)//2
            y3=(y2+y1)//2
            x4=x3
            y4=h
            cv2.line(image_copy,(x3,y3),(x4,y4),(0,0,255),2)
            continue
        if y1 > h - 5 and y2 > h - 5:
            x3 = (x2 + x1) // 2
            y3 = (y2 + y1) // 2
            x4 = x3
            y4 = 0
            cv2.line(image_copy, (x3, y3), (x4, y4), (0, 0, 255), 2)
            continue


        cv2.line(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)

# for cnt in contours:
#     x,y,w_cnt,h_cnt=cv2.boundingRect(cnt)#boundingRect表示接受轮廓所有点位，生成可以完全包裹住整条轮廓的最小外接矩形
#     #x，y：左上角坐标，w_cnt,h_cnt包围矩形长宽
#     if y<5 or (y+h_cnt)>h-5:
#         continue
#     if x<5 or (x+w_cnt)>w-5:
#         continue
#     else:
#         cv2.drawContours(image_copy,contours,-1,(0,255,0),3)

cv2.imshow('image', image)
cv2.imshow('mask_closing', mask_closing)
#cv2.imshow('res_closing', res_closing)
cv2.imshow('image_copy', image_copy)

cv2.waitKey(0)
cv2.destroyAllWindows()