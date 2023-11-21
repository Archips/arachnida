#!/usr/bin/env python3

import os
import re
import requests
import argparse
import pathlib
import signal
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

def sig_handler(sig, frame):
    sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recursive", action='store_true', help='Download recursively the images of the URL received')
    parser.add_argument("-l", "--level", nargs=1, type=int, help='if -r, indicate the depth level of the recursive download')
    parser.add_argument("-p", "--path", nargs=1, type=pathlib.Path, help='indicate the path of the downloaded images - default value is ./data')
    parser.add_argument('URL', help='Url of the site aimed to be scrapped - special character must be escape')
    args = parser.parse_args()
    
    if not args.recursive and args.level:
        parser.error("Option '-l' need option '-r'")
        sys.exit(1)

    if not url_parser(args.URL):
        print(args.URL + " : bad url")
    
    return args

def url_parser(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return 0
    return 1

def get_images_urls(site_url):
    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find_all('img')
    urls = []
    for img in img_tag:
        src = img.get('src')
        if src:
            urls.append(src)
    return urls

def download_images(img_urls, data_path, site_url):

    images_downloaded = 0
    size_download = 0.0
    for url in img_urls:
        filename = re.search(r'/([^/]+[.](svg|jpg|jpeg|png|gif|bmp))', url)
        if not filename:
            continue
        if os.path.isfile(data_path + "/" + str(filename.group(1))):
            print(f"{WARNING}{BOLD}[Already downloaded]  {END}" + filename.group(1))
            continue
        with open(data_path + "/" + str(filename.group(1)), 'wb') as f:
            if 'http' not in url:
                if url[0] == '/':
                    url = site_url + url
                else:
                    url = site_url + '/' + url
            response = requests.get(url)
            f.write(response.content)
            f.close()
            img_size = round((os.path.getsize(data_path + "/" + str(filename.group(1))) / 1024), 1)
            print(f"{GREEN}{BOLD}[Download:    " + str(img_size) + f"kb]  {END}" + filename.group(1))
            images_downloaded += 1
            size_download += img_size
    
    print(f"{GREEN}{BOLD}\nImages downloaded : " + str(images_downloaded) + " - " + str(round(size_download, 1)) + f"kb{END}")   

def spider(site_url, data_path, recursivity_level):
    while recursivity_level > 0:
        if not url_parser(site_url):
            sys.exit(1)
        img_urls = get_images_urls(site_url)
        download_images(img_urls, str(data_path), site_url)
        site_url = site_url.rsplit('/', 1)[0]
        recursivity_level -= 1

if __name__ == "__main__":

    recursivity_level = 1
    data_path = "data/"

    signal.signal(signal.SIGINT, sig_handler)

    args = parse_arguments()
    if args.recursive:
        recursivity_level =  5
    if args.level:
        recursivity_level =  int(args.level[0])
    if args.path:
        data_path = args.path[0]
    if args.URL:
        site_url = args.URL

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    if not os.access(data_path, os.R_OK | os.W_OK):
        sys.exit(1)

    os.system('clear')

    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")
    spider(site_url, data_path, recursivity_level)
    sys.exit(0)
