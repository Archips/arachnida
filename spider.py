#!/usr/bin/env python3

import os
import re
import requests
import argparse
import pathlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

BOLD = '\033[1m'
GREEN = "\033[0;32m"
WARNING = '\033[93m'
END = "\033[0m"

HEADER = """        _            _        _        _            _            _      
       / /\         /\ \     /\ \     /\ \         /\ \         /\ \    
      / /  \       /  \ \    \ \ \   /  \ \____   /  \ \       /  \ \   
     / / /\ \__   / /\ \ \   /\ \_\ / /\ \_____\ / /\ \ \     / /\ \ \  
    / / /\ \___\ / / /\ \_\ / /\/_// / /\/___  // / /\ \_\   / / /\ \_\ 
    \ \ \ \/___// / /_/ / // / /  / / /   / / // /_/_ \/_/  / / /_/ / / 
     \ \ \     / / /__\/ // / /  / / /   / / // /____/\    / / /__\/ /  
 _    \ \ \   / / /_____// / /  / / /   / / // /\____\/   / / /_____/   
/_/\__/ / /  / / /   ___/ / /__ \ \ \__/ / // / /______  / / /\ \ \     
\ \/___/ /  / / /   /\__\/_/___\ \ \___\/ // / /_______\/ / /  \ \ \    
 \_____\/   \/_/    \/_________/  \/_____/ \/__________/\/_/    \_\/    
                                                                        

"""

def parse_arguments(recursivity_level, data_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive", action='store_const', const=True, help='Download recursively the images of the URL received')
    parser.add_argument("-l", "--level", nargs=1, type=int, help='if -r, indicate the depth level of the recursive download')
    parser.add_argument("-p", "--path", nargs=1, type=pathlib.Path, help='indicate the path of the downloaded images - default value is ./data')
    parser.add_argument('URL', help='Url of the site aimed to be scrapped - special character must be escape')
    args = parser.parse_args()
    if not args.r and args.l:
        parser.error("Option '-l' need option '-r'")
        exit(1)
    elif args.r and args.l:
        recursivity_level = int(args.l[0])
    elif args.r:
        recursivity_level = 5
    if args.p:
        data_path = args.p[0]
    return recursivity_level, data_path, args.URL

def check_site(site):
    url = urlparse(site)
    if not url.scheme or not url.netloc:
        print(site + " : bad url")
        exit(1)

def get_content_from_site(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]
    return urls

def get_images(img_urls, data_path):

    images_downloaded = 0
    size_download = 0.0

    for url in img_urls:
        filename = re.search(r'/([^/]+[.](jpg|jpeg|png|gif|bmp))', url)
        if not filename:
            continue
        if os.path.isfile(data_path + str(filename.group(1))):
            print(f"{WARNING}{BOLD}[Already downloaded]  {END}" + filename.group(1))
            continue
        with open(data_path + "/" + str(filename.group(1)), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative 
                # if it is provide the base url which also happens 
                # to be the site variable atm. 
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)
            f.close()
            img_size = round((os.path.getsize(data_path + "/" + str(filename.group(1))) / 1024), 1)
            print(f"{GREEN}{BOLD}[Download:    " + str(img_size) + f"kb]  {END}" + filename.group(1))
            images_downloaded += 1
            size_download += img_size
    
    print(f"{GREEN}{BOLD}\nImages downloaded : " + str(images_downloaded) + " - " + str(round(size_download, 1)) + f"kb{END}")   

if __name__ == "__main__":

    recursivity_level = 1
    data_path = "data/"

    recursivity_level, data_path, site = parse_arguments(recursivity_level, data_path)

    check_site(site)

    if not os.path.exists(data_path):
        os.makedirs(data_path)
    os.system('clear')
    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")
    img_urls = get_content_from_site(site)
    get_images(img_urls, str(data_path))
    
    recursivity_level -= 1
    while recursivity_level > 0:
        site = site.rsplit('/', 1)[0]
        check_site(site)
        img_urls = get_content_from_site(site)
        get_images(img_urls, str(data_path))
        recursivity_level -= 1
