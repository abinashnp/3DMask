import os
import mimetypes
from src import armask
from argparse import ArgumentParser

masks = ["hat", "pirate", "hippie", "viking"]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--folder', default='vids/two',
                        help='Name of the source folder')
    parser.add_argument('--mask', default='hat',
                        help='Mask Names : \n1. hat\n2. pirate\n3. hippie\n4. viking')
    args = parser.parse_args()

    print("Starting AR Mask")

    mask_name = args.mask
    folder_name = args.folder
    mask_found = False
    for mask in masks:
        if mask == mask_name:
            mask_found = True

    if not os.path.isdir(folder_name):
        print(folder_name + " is not a valid directory")
        exit()

    if not mask_found:
        print(mask_name + " is not a valid mask name")
        exit()

    filenames = os.listdir(folder_name)

    valid_vid_paths = []

    for file in filenames:
        filepath = os.path.join(folder_name, file)
        try:
            if mimetypes.guess_type(filepath)[0].startswith('video'):
                valid_vid_paths.append(filepath)
        finally:
            print("File not a video")

    for video_file in valid_vid_paths:
        armask.process(video_file, mask_name)
