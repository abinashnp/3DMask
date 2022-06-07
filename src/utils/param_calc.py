import math
import numpy as np


def calculate_params(face_landmarks, iw, ih, idc, xd, yd, scale_factor, lat_s):
    min_x = 2000000
    min_y = 2000000
    max_x = 0
    max_y = 0

    for idx, lm in enumerate(face_landmarks):

        if lm.x * iw > max_x:
            max_x = lm.x * iw
        if lm.y * ih > max_y:
            max_y = lm.y * ih
        if lm.x * iw < min_x:
            min_x = lm.x * iw
        if lm.y * ih < min_y:
            min_y = lm.y * ih

        if idx == 152:
            pcx = lm.x * iw
            pcy = lm.y * ih
            p3x = lm.x * iw + 2000
            p3y = lm.y * ih

        if idx == 10:
            p2x = lm.x * iw
            p2y = lm.y * ih

        if idx == idc:
            p1x = lm.x * iw
            p1y = lm.y * ih

        if idx == 4:
            xC = int(lm.x * iw)
            yC = int(lm.y * ih)

        if idx == 123:
            xL = int(lm.x * iw)
            yL = int(lm.y * ih)

        if idx == 352:
            xR = int(lm.x * iw)
            yR = int(lm.y * ih)

        if idx == 10:
            xT = int(lm.x * iw)
            yT = int(lm.y * ih)

        if idx == 152:
            xB = int(lm.x * iw)
            yB = int(lm.y * ih)

    """    Calculate tilt angle of the face"""

    xangle = int(get_horizontal_angle(xC, xL, xR, yC, yL, yR))
    yangle = int(get_vertical_angle(xC, xT, xB, yC, yT, yB))

    yangle = -yangle

    if yangle == 90:
        yangle = 0
    """Calculate the target width and target height of the face mesh"""
    tw = int(max_x - min_x)
    th = int(max_y - min_y)

    tw = int(tw * scale_factor * (1 - 2 * xd) * ((90 + math.fabs(0.3 * xangle)) / 90))
    th = int(th * scale_factor * (1 - 2 * yd))
    """Calculate the tilt angle of the face"""
    tilt_angle = int(360 - angle3pt((p3x, p3y), (pcx, pcy), (p2x, p2y)))

    xd = tw * xd
    yd = th * yd
    mx = int(p1x + xd)
    my = int(p1y + yd)
    nx, ny = rotate((mx, my), (p1x, p1y), -(tilt_angle - 90))
    nx = int(nx)
    ny = int(ny)

    # x coordinate of overlay position
    ocx = int(nx + ((xangle / 90) * tw) / 3)

    # y coordinate of overlay position
    ocy = int(ny + ((yangle / 90) * th) / 3)

    if xangle > 0:
        ocx = ocx - (tw * lat_s * math.fabs((xangle / 90)))
    else:
        ocx = ocx + (tw * lat_s * math.fabs((xangle / 90)))

    return xangle, yangle, tw, th, tilt_angle, ocx, ocy


def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def get_horizontal_angle(xC, xL, xR, yC, yL, yR):
    dL = math.sqrt(((xC - xL) ** 2) + ((yC - yL) ** 2))
    dR = math.sqrt(((xC - xR) ** 2) + ((yC - yR) ** 2))
    dT = dL + dR
    dH = dT / 2
    if dL >= dR:
        if xC >= xR:
            x_angle = -(45 + ((dR / dL) * 45))
        else:
            x_angle = -(45 - ((dR / dH) * 45))
    else:
        if xC <= xL:
            x_angle = 45 + ((dL / dR) * 45)
        else:
            x_angle = 45 - ((dL / dH) * 45)

    return x_angle


def get_vertical_angle(xC, xL, xR, yC, yL, yR):
    dL = math.sqrt(((xC - xL) ** 2) + ((yC - yL) ** 2))
    dR = math.sqrt(((xC - xR) ** 2) + ((yC - yR) ** 2))
    dT = dL + dR
    dH = dT / 2
    if dL >= dR:
        if yC >= yR:
            y_angle = -(45 + ((dR / dL) * 45))
        else:
            y_angle = -(45 - ((dR / dH) * 45))
    else:
        if yC <= yL:
            y_angle = 45 + ((dL / dR) * 45)
        else:
            y_angle = 45 - ((dL / dH) * 45)

    return y_angle


def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T - o.T) + o.T).T)
