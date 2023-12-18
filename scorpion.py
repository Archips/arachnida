#!/usr/bin/env python

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
from exif import Image
import webbrowser

BOLD = '\033[1m'
GREEN = "\033[0;32m"
WARNING = '\033[93m'
END = "\033[0m"
EXIF_MEMBER = ["delete", "delete_all", "get", "get_all", "get_file", "get_thumbnail", "list_all", "has_exif", "set"]

HEADER = """
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
    
        
    """
    
    Signal handler for SIGINT (Ctrl+C).
    Exits the program with status code 1.
    
    """

    sys.exit(1)

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('IMG', nargs='+', help='images path')
    args = parser.parse_args()
    return args

def basic_metadata(image, image_members):

    print(f"{GREEN}{BOLD}Metadata{END}")
    print("--------------------\n")
    print(f"")

def date_time_exif(image, image_members):

    if 'datetime_original' in image_members:
        print(f"{GREEN}{BOLD}Date - Time{END}")
        print("--------------------\n")
        print(f"{BOLD}Original datetime: {END}{image.get('datetime_original', 'Unkown')}")
        if 'offset_time' in image_members:
            print(f"{BOLD}Datetime offset UTC: {END}{image.get('offset_time')}")
        if 'datetime' in image_members:
            print(f"{BOLD}Datetime: {END}{image.get('datetime')}")
        if 'datetime_digitized' in image_members:
            print(f"{BOLD}Datetime digitized: {END}{image.get('datetime_digitized')}")
        print("")

def format_dms_coordinates(coordinates):
    return f"{coordinates[0]}° {coordinates[1]}\' {coordinates[2]}\""

def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref):
    
    decimal_latitude = dms_coordinates_to_dd_coordinates(latitude, latitude_ref)
    decimal_longitude = dms_coordinates_to_dd_coordinates(longitude, longitude_ref)
    url = f"https://www.google.com/maps?q={decimal_latitude},{decimal_longitude}"
    webbrowser.open(url)

def geo_location_exif(image, image_members):

    if 'gps_latitude' in image_members:
        print(f"{GREEN}{BOLD}Coordinates{END}")
        print("---------------------")
        print(f"Latitude (DMS): {format_dms_coordinates(image.gps_latitude)} {image.gps_latitude_ref}")
        print(f"Longitude (DMS): {format_dms_coordinates(image.gps_longitude)} {image.gps_longitude_ref}\n")
        print(f"Latitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_latitude, image.gps_latitude_ref)}")
        print(f"Longitude (DD): {dms_coordinates_to_dd_coordinates(image.gps_longitude, image.gps_longitude_ref)}\n")

        draw_map_for_location(image.gps_latitude, 
                              image.gps_latitude_ref, 
                              image.gps_longitude,
                              image.gps_longitude_ref)

def device_exif(image, image_members):
    
    if 'make' in image_members:
        print(f"{GREEN}{BOLD}Device information{END}")
        print("--------------------\n")
        print(f"{BOLD}Make: {END}{image.make}")
        print(f"{BOLD}Model: {END}{image.model}\n")

def lens_exif(image, image_members):

    if 'lens_make' in image_members:
        print(f"{GREEN}{BOLD}Lens and OS{END}")
        print("--------------------\n")
        print(f"{BOLD}Lens make: {END}{image.get('lens_make', 'Unkown')}")
        if 'lens_model' in image_members:
            print(f"{BOLD}Lens model: {END}{image.get('lens_model', 'Unkown')}")
        if 'lens_specification' in image_members:
            print(f"{BOLD}Lens specification: {END}{image.get('lens_specification', 'Unkown')}")
        if 'software' in image_members:
            print(f"{BOLD}OS version: {END}{image.get('software', 'Unkown')}\n")

def scorpion(img_path):

    with open(img_path, "rb") as image_file:
        image = Image(image_file)

    try:
        status = f"{GREEN}{BOLD}EXIF version: {END}{image.exif_version}\n"
        print(status)
    except:
        print("Image does not contain any EXIF information.\n")
        return


    image_members = dir(image)
    print(f"*** {image_members} ***\n")
    date_time_exif(image, image_members)
    basic_metadata(image, image_members) 
    geo_location_exif(image, image_members)
    device_exif(image, image_members)
    lens_exif(image, image_members)

if __name__ == "__main__":
    
    args = parse_arguments()
    
    signal.signal(signal.SIGINT, sig_handler)

    os.system('clear')
    
    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")
    for arg in args.IMG:
        print(f"{GREEN}{BOLD}\nImage : [" + arg + f"]{END}\n")
        scorpion(arg)

    sys.exit(0)
