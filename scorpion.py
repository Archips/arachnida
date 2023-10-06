#!/usr/bin/env python3

import os
import sys
import argparse
import pathlib
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

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('IMG', nargs='*', help='images path')
    args = parser.parse_args()
    return args

def scorpion(img):

    try:
        image = Image.open(img)
    except:
        print(f"{WARNING}{BOLD}Image : [" + img + f"] is unreadable{END}")
        return

    print(f"{BOLD}Metadata\n{END}");
    # extract other basic metadata
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    for label,value in info_dict.items():
        print(f"{label:25}: {value}")
    
    # extract EXIF data
    exifdata = image.getexif()

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

if __name__ == "__main__":
    
    args = parse_arguments()

    os.system('clear')
    
    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")
    for arg in args.IMG:
        print(f"{GREEN}{BOLD}\nImage : [" + arg + f"]{END}\n")
        scorpion(arg)

    exit(0)
