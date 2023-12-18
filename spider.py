#!/usr/bin/env python

"""
spider.py - A script for web scraping images from a website.

Usage:
    spider.py [-r] [-l LEVEL] [-p PATH] URL

Options:
    -r, --recursive     Download images recursively from the URL.
    -l LEVEL, --level LEVEL    Set the depth level for recursive download.
    -p PATH, --path PATH      Set the path for downloaded images (default is ./data).
    URL                 URL of the site to be scraped (special characters must be escaped).

Description:
    This script takes a website URL as input and downloads images from the specified site.
    Options allow for recursive download, setting the depth level, and specifying the download path.

Dependencies:
    - Python 3
    - requests library for HTTP requests
    - BeautifulSoup (bs4) library for HTML parsing

"""

import os
import re
import requests
import argparse
import pathlib
import signal
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

BOLD = '\033[1m'
RED = "\033[0;31m"
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
    
    """
    
    Signal handler for SIGINT (Ctrl+C).
    Exits the program with status code 1.
    
    """

    sys.exit(1)

def parse_arguments():

    """
    
    Parse command line arguments.

    Returns:
    argparse.Namespace: The parsed arguments.
    
    """
    
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
        print(f"{RED}{BOLD}" + args.URL + f" : bad url\n{END}")
    
    return args

def url_parser(url):
    
    """
    
    Parse and validate the URL.

    Parameters:
    - url (str): The URL to be parsed.

    Returns:
    int: 1 if the URL is valid, 0 otherwise.
    
    """

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return 0
    return 1

def get_images_urls(site_url):

    """
    
    Retrieve image URLs from the specified site URL.

    Parameters:
    - site_url (str): The URL of the site to be scraped.

    Returns:
    list: List of image URLs.

    Raises:
    - requests.exceptions.Timeout: If the request times out.
    - requests.exceptions.HTTPError: If an HTTP error occurs.
    - requests.exceptions.RequestException: If a general request exception occurs.
    - requests.exceptions.ConnectionError: If a connection error occurs.
    
    """

    try:
        response = requests.get(site_url)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"{RED}{BOLD}The request timed out.{END}\n")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"{RED}{BOLD}HTTP Error: {e}{END}\n")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"{RED}{BOLD}An error occurred: {e}{END}\n")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"{RED}{BOLD}A connection error occurred. Please check your internet connection.{END}\n")
        sys.exit(1)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find_all('img')
    urls = []
    for img in img_tag:
        src = img.get('src')
        if src:
            urls.append(src)
    return urls

def download_images(img_urls, data_path, site_url):

    """

    Download images from the provided URLs.

    Parameters:
    - img_urls (list): List of image URLs.
    - data_path (str): Path where the images will be saved.
    - site_url (str): The base URL of the site.

    Returns:
    None

    Raises:
    - requests.RequestException: If an error occurs during image download.
    
    """

    images_downloaded = 0
    size_download = 0.0
    for url in img_urls:
        filename = re.search(r'/([^/]+[.](jpg|jpeg|png|gif|bmp))', url)
        if not filename:
            continue
        if os.path.isfile(data_path + "/" + str(filename.group(1))):
            print(f"{WARNING}{BOLD}[Already downloaded]   {END}" + filename.group(1))
            continue
        with open(data_path + "/" + str(filename.group(1)), 'wb') as f:
            try:
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
            except requests.RequestException as e:
                print(f"{RED}{BOLD}Error downloading {url}: {e}{END}\n")
                continue

    print(f"{GREEN}{BOLD}\nImages downloaded : " + str(images_downloaded) + " - " + str(round(size_download, 1)) + f"kb{END}")   

def spider(site_url, data_path, recursivity_level):
    
    """
    
    Perform web scraping of images recursively.

    Parameters:
    - site_url (str): The URL of the site to be scraped.
    - data_path (str): Path where the images will be saved.
    - recursivity_level (int): Depth level for recursive download.

    Returns:
    None

    Raises:
    - sys.exit(1): If the URL is invalid.
    
    """

    while recursivity_level > 0:
        if not url_parser(site_url):
            sys.exit(1)
        img_urls = get_images_urls(site_url)
        download_images(img_urls, str(data_path), site_url)
        site_url = site_url.rsplit('/', 1)[0]
        recursivity_level -= 1

def display_header():
    
    """
    
    Display the header content.

    Returns:
    None
    
    """

    os.system('clear')
    print(f"{GREEN}{BOLD}" + HEADER + f"{END}")


if __name__ == "__main__":

    recursivity_level = 1
    data_path = "data/"
    
    display_header()

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

    spider(site_url, data_path, recursivity_level)
    
    sys.exit(0)
