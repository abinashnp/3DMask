import os.path

from src.utils import fmm as face_mesh
import numpy as np
from tqdm import tqdm
import cv2
import moviepy.editor as mp
from moviepy.editor import *



def start(mask):
    an_cap = cv2.VideoCapture(0)

    # frame per second of original video
    fps = an_cap.get(cv2.CAP_PROP_FPS)

    # Calculate total number of frame
    total_frames = int(an_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get mesh object from face mesh module
    mesh = face_mesh.FaceMeshModule()

    # Read frame
    success, img = an_cap.read()

    # Read image width and height
    img_height, img_width, _ = img.shape


    while an_cap.isOpened():

        success, img = an_cap.read()
        img = cv2.flip(img, 1)
        if success:

            x, y, tw, th, tilt_angle, ocx, ocy = mesh.get_landmark_data(img, filter_name=mask)

            try:
                img = mesh.apply_filter(img,
                                        x_angle=x,
                                        y_angle=y,
                                        tiltangle=tilt_angle,
                                        tw=tw,
                                        th=th,
                                        ocx=ocx,
                                        ocy=ocy, filtername=mask)
            except:
                s=2

            cv2.imshow("processed", img)
            cv2.waitKey(1)
        else:
            break

    cv2.destroyAllWindows()


def process(file_name=os.getcwd() + '/sample.mp4', mask="viking"):
    print(os.getcwd())
    f_name = file_name.split(".")[0]
    ext = file_name.split(".")[1]
    out_name = f_name + "_out." + ext
    should_flip = False
    window_size = 3
    start(mask)

process()