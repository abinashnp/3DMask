import os.path

from src.utils import fmm as face_mesh
import numpy as np
from tqdm import tqdm
import cv2
import moviepy.editor as mp
from moviepy.editor import *


def smooth_data_moving_average(array, window):
    arr = array
    window_size = window
    len_array = len(arr)
    index = 0
    # Initialize an empty list to store moving averages
    moving_averages = []
    for x in range(int(window / 2)):
        moving_averages.append(arr[x])
    # Loop through the array to
    # consider every window of size 3
    while index < len(arr) - window_size + 1:
        # Calculate the average of current window
        window_average = round(np.sum(arr[
                                      index:index + window_size]) / window_size, 2)

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)

        # Shift window to right by one position
        index += 1
    for y in reversed(range(int(window / 2))):
        moving_averages.append(arr[len_array - y - 1])
    return moving_averages


def start(fileName, out_name, mask, shouldFlip, window_size, should_resize, w, h):
    print("Analyzing video " + fileName + " ...")

    video = mp.VideoFileClip(fileName)

    has_audio = False
    if video.audio:
        has_audio = True
        video.audio.write_audiofile("temp.mp3")

    an_cap = cv2.VideoCapture(fileName)

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

    i_height = img_height
    i_width = img_width

    if should_resize is True:
        i_height = h
        i_width = w

    # Initialize output video writer
    if has_audio:
        writer = cv2.VideoWriter("temp.mp4", cv2.VideoWriter_fourcc(*'DIVX'), int(fps), (i_width, i_height))
    else:
        writer = cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*'DIVX'), int(fps), (i_width, i_height))

    """Data Array Initialization"""
    x_angle_list = []
    y_angle_list = []
    tilt_angle_list = []
    t_w_list = []
    t_h_list = []
    o_cx_list = []
    o_cy_list = []
    frame_available = []

    # Re-initialize video
    an_cap = cv2.VideoCapture(fileName)

    # Previous Data
    p_x = 0
    p_y = 0
    p_tw = 0
    p_th = 0
    p_tilt_angle = 0
    p_ocx = 0
    p_ocy = 0

    """Get Data from Face Mesh Module"""
    with tqdm(total=total_frames) as pbar:
        while an_cap.isOpened():

            success, img = an_cap.read()
            if shouldFlip is True:
                img = cv2.flip(img, 1)
            if success:
                x, y, tw, th, tilt_angle, ocx, ocy = mesh.get_landmark_data(img, filter_name=mask)

                # Read and append the value
                if x is not None:
                    x_angle_list.append(x)
                    p_x = x
                else:
                    x_angle_list.append(p_x)

                if y is not None:
                    y_angle_list.append(y)
                    p_y = y
                else:
                    y_angle_list.append(p_y)

                if tilt_angle is not None:
                    tilt_angle_list.append(tilt_angle)
                    p_tilt_angle = tilt_angle
                else:
                    tilt_angle_list.append(p_tilt_angle)

                if tw is not None:
                    t_w_list.append(tw)
                    p_tw = tw
                else:
                    t_w_list.append(p_tw)

                if th is not None:
                    t_h_list.append(th)
                    p_th = th
                else:
                    t_h_list.append(p_th)

                if ocx is not None:
                    o_cx_list.append(ocx)
                    p_ocx = ocx
                else:
                    o_cx_list.append(p_ocx)

                if ocy is not None:
                    o_cy_list.append(ocy)
                    frame_available.append(True)
                    p_ocy = ocy
                else:
                    o_cy_list.append(p_ocy)
                    frame_available.append(False)

            else:
                break
            pbar.update(1)

    an_cap.release()

    print("Processing video " + fileName + " ...")

    """Smooth the landmark data with moving average"""
    x_angle_list = smooth_data_moving_average(x_angle_list, 3)
    y_angle_list = smooth_data_moving_average(y_angle_list, 3)
    tilt_angle_list = smooth_data_moving_average(tilt_angle_list, 5)

    t_w_list = smooth_data_moving_average(t_w_list, window_size)
    t_h_list = smooth_data_moving_average(t_h_list, window_size)

    o_cx_list = smooth_data_moving_average(o_cx_list, window_size)
    o_cy_list = smooth_data_moving_average(o_cy_list, window_size)

    frame = 0

    # Re-initialize video
    an_cap = cv2.VideoCapture(fileName)

    """Get Data from Face Mesh Module"""
    with tqdm(total=total_frames) as pbar:
        while an_cap.isOpened():

            success, img = an_cap.read()

            if success:

                if shouldFlip is True:
                    img = cv2.flip(img, 1)

                if frame_available[frame]:
                    img = mesh.apply_filter(img,
                                            x_angle=int(x_angle_list[frame]),
                                            y_angle=int(y_angle_list[frame]),
                                            tiltangle=tilt_angle_list[frame],
                                            tw=int(t_w_list[frame]),
                                            th=int(t_h_list[frame]),
                                            ocx=int(o_cx_list[frame]),
                                            ocy=int(o_cy_list[frame]), filtername=mask)

                if should_resize is True:
                    img = cv2.resize(img, (i_width, i_height))
                frame = frame + 1
                writer.write(img)
            else:
                break
            pbar.update(1)

    an_cap.release()

    writer.release()

    if has_audio:
        video_clip = VideoFileClip("temp.mp4")
        audio_clip = AudioFileClip("temp.mp3")

        new_audio_clip = CompositeAudioClip([audio_clip])
        video_clip.audio = new_audio_clip
        video_clip.write_videofile(out_name)

        os.remove("temp.mp4")
        os.remove("temp.mp3")

    cv2.destroyAllWindows()


def process(file_name=os.getcwd() + '/sample.mp4', mask="hat", should_resize=False, w=0, h=0):
    print(os.getcwd())
    f_name = file_name.split(".")[0]
    ext = file_name.split(".")[1]
    out_name = f_name + "_out." + ext
    should_flip = False
    window_size = 3
    print(w, h)
    start(file_name, out_name, mask, should_flip, window_size, should_resize, w, h)
