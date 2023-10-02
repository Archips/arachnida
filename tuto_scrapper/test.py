#!/usr/bin/env python3

import re
import requests
import pathlib
import argparse
from bs4 import BeautifulSoup

def parse_arguments(recursivity_level, data_path):
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_const', const=True)
    parser.add_argument("-l", nargs=1, type=int)
    parser.add_argument("-p", nargs=1, type=pathlib.Path)
    args = parser.parse_args()
    if not args.r and args.l:
        parser.error("Option '-l' need option '-r'")
        exit(1)
    elif args.r and args.l:
        recursivity_level = args.l
    elif args.r:
        recursivity_level = 5
    if args.p:
        data_path = args.p

def get_content_from_site(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]
    return urls

def get_images(img_urls):
    for url in img_urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg|png|gif|bmp))$', url)
        if not filename:
            continue
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative 
                # if it is provide the base url which also happens 
                # to be the site variable atm. 
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)

if __name__ == "__main__":

    recursivity_level = 0
    data_path = "data/"

    parse_arguments(recursivity_level, data_path)

    print(recursivity_level)
    print(data_path)

    site = 'http://www.github.com/Archips'
    img_urls = get_content_from_site(site)
    get_images(img_urls)

