import cv2
import os

img = cv2.imread('../render/hat_0_0.jpg', cv2.IMREAD_COLOR)

text_file = open("../render/data.txt", "w")
text_file.write(str(img))
text_file.close()

print(img.shape)
img = cv2.resize(img, (300, 300))

while True:
    cv2.imshow("hh", img)
    cv2.waitKey(1)
