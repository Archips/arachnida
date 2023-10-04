#!/usr/bin/env python3

import os
import re
import requests
import argparse
import pathlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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
    return 0


def scorpion(img):

    image = Image.open(img)
 
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
    scorpion("/mnt/nfs/homes/athirion/Pictures/athirion.jpg")
    exit(0)
