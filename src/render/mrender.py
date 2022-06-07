import cv2
from PIL import Image
import numpy as np


def getImg(xangle, yangle, model):
    x = (int(xangle / 2) * 2)
    y = (int(yangle / 2) * 2)

    fname = '../render/imgs/' + str(model) + '/' + str(model) + '_' + str(x) + '_' + str(y) + '.jpg'
    imgp = Image.open(fname)
    img = np.array(imgp)
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    return img


def show():
    img = getImg(-8, 2, "hat")
    while True:
        cv2.imshow("ss", img)
        cv2.waitKey(0)

show()
