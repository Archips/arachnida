#!/usr/bin/env python3

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

HEADER = """

                               ..
                        .!5B&@@@@&P~
                      :B@@@@@B7~@@@@5
                     ^@@@G:.    Y@@@#
                     Y@@@J       ?@&
                     7@@@?        ^G.
                     ?@@@@.
                     ^@@@@7
                      7@@@&~
                      ~@@@@@:
                       P@@@@B:
                        @@@@@@!
                        7@@@@@@?.
                         .&@@@@@@&Y:      ..
                          5@@@@@@@@@&P7?GG5&&.
                          :@@@@@@@@@@@@@@P..B@7.~^
                           #@@@@@@@@@@@@@@@&Y&@@?&@:
                           !@@@@@@@@@@@@@@@@@@@@J.&@77JYY
                            &@@@@@@@@@@@@@@@@@@@@@@@@7^~@Y  J7^
                     .~?5GGP&@@@@@@@@@@@@@@@@@@@@@@@@G~ PG B&~P&7.!JY55YJ7~:.
                 .~5BP?JJ!^.^#@@@@@@@@@@@@@@@@@@@@@@@@@@@&?&:  .@@@@@@@@@@@@@@&BY~.
             :!?YY?^          .?G@@@@@@@@@@@@@@@@@@@@@@@@@@@~  !@@@@@7 :&@@@@@@@@@@B!
                             .^7J#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#7    7P#@@@@@@@@@&~
                         .?B&&G!::^7YP#@@@@@@@@@@@@@@@@@@@@@@@@@&^           :~777!75@@#:
                       !B#5~.        :&&5GGP?7G##BB@@@@@@@@@P.:.                     :@@@J
                    .7G5:           Y@5       .~?JY#@@@@@@B^           .:^^^:.        ?#G@B^:.         ..:^^^:.      ...........      ............      ....      ..:^^^:.      ......      .....
                  .~!:             ?@?       5&~...7@@@@P:          ~#@@@@@@@@@B^  .Y&@@@@@@@@@#J   .P&@@@@@@@@@B7   &@@@@@@@@@@@  G@@@@@@@@@@@@#Y  7@@@@~  ^G&@@@@@@@@&B~  .@@@@@@5.   .@@@@5
                                  :@J       G@.   :@@@@.           ^@@@@@Y7JGGP5? .@@@@&!:.:?###&Y ^@@@@#~..:J@@@@B  @@@@&....:P@@@@! B@@@@:....7@@@@P 7@@@@~ 7@@@@G^..^5@@@@5 .@@@@&@@@?  .@@@@5
                                 .&?       J@.    G@@@B!5#&&&G7.    Y#&@@@@@@@&#? J@@@@^           P@@@@.     G@@@@. &@@@@BBBB#@@@@#. G@@@@BBBB#&@@@@~ 7@@@@~ #@@@@      #@@@@ .@@@@5 P@@&~.@@@@5
                                :P:       ~@!     5@@@@@@@@@@@@@P.  Y5PGG?!Y@@@@@..@@@@&!:.:J##&&Y ^@@@@#!::^Y@@@@G  @@@@@PPPG&@@@&~  B@@@@GPPPP5J7^   7@@@@~ !@@@@B~::^P@@@@5 .@@@@5  :B@@&@@@@5
                               .7        .@5       @@@@@@@@@@@@@@@^ ~#@@@@@@@@&G:  .Y&@@@@@@@@@#?   .5&@@@@@@@@&B!   &@@@B     Y@@@@. G@@@@            !@@@@~  :P&@@@@@@@@&G~  .@@@@5    ~&@@@@@5
                                         ?B        J@@@@@@@@@@@@@@@5:..:^~~^:.         .::^::.          .:^^::.      .....      ....  .....             ....      ..:^^:..      ....       .....
                                         .          ^B@@@@@@@@@@@@@@@@@@@&&G!
                                                      .7B@@@@@@@@@@#PJ7~^:.
                                                          ~5&@@@@@@!.
                                                             .^75G#&&#BPY?777:
                                                                      .....

"""                                                                      

# HEADER = """        _            _        _        _            _            _      
#         _             _             _            _           _        _          _            _          
#        / /\         /\ \           /\ \         /\ \        /\ \     /\ \       /\ \         /\ \     _  
#       / /  \       /  \ \         /  \ \       /  \ \      /  \ \    \ \ \     /  \ \       /  \ \   /\_
#      / / /\ \__   / /\ \ \       / /\ \ \     / /\ \ \    / /\ \ \   /\ \_\   / /\ \ \     / /\ \ \_/ / /
#     / / /\ \___\ / / /\ \ \     / / /\ \ \   / / /\ \_\  / / /\ \_\ / /\/_/  / / /\ \ \   / / /\ \___/ / 
#     \ \ \ \/___// / /  \ \_\   / / /  \ \_\ / / /_/ / / / / /_/ / // / /    / / /  \ \_\ / / /  \/____/  
#      \ \ \     / / /    \/_/  / / /   / / // / /__\/ / / / /__\/ // / /    / / /   / / // / /    / / /   
#  _    \ \ \   / / /          / / /   / / // / /_____/ / / /_____// / /    / / /   / / // / /    / / /    
# /_/\__/ / /  / / /________  / / /___/ / // / /\ \ \  / / /   ___/ / /__  / / /___/ / // / /    / / /     
# \ \/___/ /  / / /_________\/ / /____\/ // / /  \ \ \/ / /   /\__\/_/___\/ / /____\/ // / /    / / /      
#  \_____\/   \/____________/\/_________/ \/_/    \_\/\/_/    \/_________/\/_________/ \/_/     \/_/       
                                                                                                         

# """

def sig_handler(sig, frame):
    exit(1)

def parse_arguments():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('IMG', nargs='*', help='images path')
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
            value = value.decode()
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

    exit(0)
