import cv2
import os

img = cv2.imread('../render/imgs/hat/hat_-8_2.jpg', cv2.IMREAD_COLOR)

print(img.shape)
img=cv2.resize(img,(300,300))

while True:
    cv2.imshow("hh", img)
    cv2.waitKey(1)
