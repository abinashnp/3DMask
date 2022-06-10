import os
import mimetypes
from src import armask
from argparse import ArgumentParser

masks = ["hat", "pirate", "hippie", "viking"]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--file', default='sample.mp4',
                        help='Name of the file')
    parser.add_argument('--mask', default='hat',
                        help='Mask Names : \n1. hat\n2. pirate\n3. hippie\n4. viking')
    args = parser.parse_args()

    print("Starting AR Mask")

    mask_name = args.mask
    file_name = args.file
    mask_found = False
    for mask in masks:
        if mask == mask_name:
            mask_found = True

    if not mask_found:
        print(mask_name + " is not a valid mask name")
        exit()

    if not mimetypes.guess_type(file_name)[0].startswith('video'):
        print(file_name + " is not a video file")
        exit()

    armask.process(file_name, mask_name)
