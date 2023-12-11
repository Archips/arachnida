#!/usr/bin/env python3

"""
scorpion.py - A script to extract metadata and Exif data from images.

Usage:
    scorpion.py IMG [IMG ...]

Options:
    IMG         Path(s) to the image file(s).

Description:
    This script takes one or more image file paths as input and extracts metadata
    as well as Exif data from each image. The extracted information includes
    basic details such as filename, image format, size, height, width, mode,
    palette, animation status, and the number of frames. Additionally, it extracts
    Exif data if available.

Dependencies:
    - Python 3
    - Pillow (PIL) library for image processing

"""

import os
import sys
import argparse
import pathlib
import signal
from PIL import Image
from PIL.ExifTags import TAGS

BOLD = '\033[1m'
GREEN = "\033[0;32m"
WARNING = '\033[93m'
END = "\033[0m"

HEADER = """        _            _        _        _            _            _      
        _             _             _            _           _        _          _            _          
       / /\         /\ \           /\ \         /\ \        /\ \     /\ \       /\ \         /\ \     _  
      / /  \       /  \ \         /  \ \       /  \ \      /  \ \    \ \ \     /  \ \       /  \ \   /\_
     / / /\ \__   / /\ \ \       / /\ \ \     / /\ \ \    / /\ \ \   /\ \_\   / /\ \ \     / /\ \ \_/ / /
    / / /\ \___\ / / /\ \ \     / / /\ \ \   / / /\ \_\  / / /\ \_\ / /\/_/  / / /\ \ \   / / /\ \___/ / 
    \ \ \ \/___// / /  \ \_\   / / /  \ \_\ / / /_/ / / / / /_/ / // / /    / / /  \ \_\ / / /  \/____/  
     \ \ \     / / /    \/_/  / / /   / / // / /__\/ / / / /__\/ // / /    / / /   / / // / /    / / /   
 _    \ \ \   / / /          / / /   / / // / /_____/ / / /_____// / /    / / /   / / // / /    / / /    
/_/\__/ / /  / / /________  / / /___/ / // / /\ \ \  / / /   ___/ / /__  / / /___/ / // / /    / / /     
\ \/___/ /  / / /_________\/ / /____\/ // / /  \ \ \/ / /   /\__\/_/___\/ / /____\/ // / /    / / /      
 \_____\/   \/____________/\/_________/ \/_/    \_\/\/_/    \/_________/\/_________/ \/_/     \/_/       
                                                                                                         

"""

def sig_handler(sig, frame):
    sys.sys.exit(1)

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('IMG', nargs='+', help='images path')
    args = parser.parse_args()
    return args


def extract_metadata(image):
    print(f"{BOLD}Metadata\n{END}");
    # extract other basic metadata
    info_dict = {
        "Filename": image.filename,
        "Image Format": image.format,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Mode": image.mode,
        "Image Color": image.palette,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    for label,value in info_dict.items():
        print(f"{label:25}: {value}")

    for label, value in image.info.items():
        if isinstance(value, bytes):
            try:
                value = value.decode()
            except:
                continue
        print(f"{label:25}: {value}")


def extract_exif(image):
    # extract EXIF data
    exifdata = image.getexif()

    if not exifdata:
        print(f"{WARNING}{BOLD}\nNo exif data\n{END}");
        return

    print(f"{BOLD}\nExif\n{END}");
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")


def scorpion(img):

    try:
        image = Image.open(img)
    except:
        print(f"{WARNING}{BOLD}Image data is unreadable{END}")
        return

    extract_metadata(image)
    extract_exif(image)


if __name__ == "__main__":
    
    args = parse_arguments()
    
    signal.signal(signal.SIGINT, sig_handler)

    os.system('clear')
    
    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")
    for arg in args.IMG:
        print(f"{GREEN}{BOLD}\nImage : [" + arg + f"]{END}\n")
        scorpion(arg)

    sys.exit(0)
