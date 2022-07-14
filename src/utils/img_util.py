import cv2
import numpy as np


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def overlay_transparent(bg, overlay, px, py):
    b_width = bg.shape[1]
    b_height = bg.shape[0]

    o_width = overlay.shape[1]
    o_height = overlay.shape[0]

    padding_x = min(px, b_width - px)
    padding_y = min(py, b_height - py)

    nL = b_width

    if padding_x < o_width / 2 or padding_y < o_height / 2:
        nL = 0

    x = px + nL
    y = py + nL

    background = cv2.resize(bg, (b_width + 2 * nL, b_height + 2 * nL))
    background[nL:nL + b_height, nL:nL + b_width] = bg

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y + h, x:x + w] = (1.0 - mask) * background[y:y + h, x:x + w] + mask * overlay_image

    # print(background.shape)
    new_crop = background[nL:nL + b_height, nL:nL + b_width]

    # print(new_crop.shape)
    return new_crop
