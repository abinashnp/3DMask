import cv2
import mediapipe as mp
import numpy as np
import os
from src.config import filterconfig
from src.utils.img_util import overlay_transparent, rotate_image
from src.utils.param_calc import calculate_params


def insert_overlay(img, tiltangle, tw, th, oCx, oCy, xangle, yangle,
                   hor_s, ver_s, filtername, trim, threshold):
    x = (int(xangle / 2) * 2)
    y = (int(yangle / 2) * 2)
    fname = os.path.join(os.getcwd(), 'src', 'utils', 'imgs', str(filtername),
                         str(filtername) + '_' + str(x) + '_' + str(y) + '.jpg')

    mimg = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

    if tw > th:
        nw = tw
    else:
        nw = th

    mimg = cv2.resize(mimg, (int(nw * hor_s), int(nw * ver_s)))

    mimg = rotate_image(mimg, tiltangle)

    na = cv2.cvtColor(mimg, cv2.COLOR_BGR2RGB)
    alpha = np.sum(na, axis=-1) > threshold
    # Convert True/False to 0/255 and change type to "uint8" to match "na"
    alpha = np.uint8(alpha * 255)
    # Stack new alpha layer with existing image to go from BGR to BGRA, i.e. 3 channels to 4 channels
    res = np.dstack((na, alpha))
    # Stack new alpha layer with existing image to go from BGR to BGRA, i.e. 3 channels to 4 channels
    overlay = res
    # overlay = cv2.imread("horn.png", cv2.IMREAD_UNCHANGED)
    # tw, th = self.stablizeshape(tw, th)

    y, x = overlay[:, :, 3].nonzero()  # get the nonzero alpha coordinates

    if (trim):
        min_x = np.min(x)
        min_y = np.min(y)
        max_x = np.max(x)
        max_y = np.max(y)

        overlay = overlay[min_y:max_y, min_x:max_x]

    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGBA)

    cx = int(oCx - (overlay.shape[1] / 2))
    cy = int(oCy - (overlay.shape[0] / 2))
    return overlay_transparent(img, overlay, cx, cy)


class FaceMeshModule:
    def __init__(self):
        super().__init__()

        self.face_mesh = mp.solutions.face_mesh
        self.mesh = self.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=False, min_tracking_confidence=0.2,
                                            min_detection_confidence=0.2)
        self.prev_t_w = None
        self.prevth = None

        self.prev_angle = None

    def get_landmark_data(self, img, filter_name="hat"):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.mesh.process(imgRGB)

        imgHeight, imgWidth, _ = img.shape
        x = None
        y = None
        tw = None
        th = None
        tilt_angle = None
        ocx = None
        ocy = None

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                modelName, albedoName, scalefactor, xdeflection, ydeflection, idA, idB, _, _, _, lat_s, _, _ = filterconfig.get_config(
                    filter_name)

                x, y, tw, th, tilt_angle, ocx, ocy = calculate_params(face_landmarks.landmark, imgWidth,
                                                                      imgHeight,
                                                                      idA,
                                                                      xdeflection, ydeflection, scalefactor,
                                                                      lat_s)

        return x, y, tw, th, tilt_angle, ocx, ocy

    def apply_filter(self, img, x_angle, y_angle, tiltangle, tw, th, ocx, ocy, filtername="hat"):
        modelName, albedoName, scalefactor, xdeflection, ydeflection, idA, idB, cameraeye, hor_s, ver_s, _, trim, threshold = filterconfig.get_config(
            filtername)
        return insert_overlay(img=img,
                              tiltangle=tiltangle - 90,
                              tw=tw,
                              th=th,
                              oCx=ocx,
                              oCy=ocy, xangle=x_angle, yangle=y_angle, hor_s=hor_s,
                              ver_s=ver_s,
                              filtername=filtername,
                              trim=trim,
                              threshold=threshold
                              )
