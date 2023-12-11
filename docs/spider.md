<!-- markdownlint-disable -->

<a href="../spider.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `spider.py`
spider.py - A script for web scraping images from a website. 

Usage:  spider.py [-r] [-l LEVEL] [-p PATH] URL 

Options: 
    -r, --recursive     Download images recursively from the URL. 
    -l LEVEL, --level LEVEL    Set the depth level for recursive download. 
    -p PATH, --path PATH      Set the path for downloaded images (default is ./data).  URL                 URL of the site to be scraped (special characters must be escaped). 

Description:  This script takes a website URL as input and downloads images from the specified site.  Options allow for recursive download, setting the depth level, and specifying the download path. 

Dependencies: 
    - Python 3 
    - requests library for HTTP requests 
    - BeautifulSoup (bs4) library for HTML parsing 

**Global Variables**
---------------
- **BOLD**
- **RED**
- **GREEN**
- **WARNING**
- **END**
- **HEADER**

---

<a href="../spider.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sig_handler`

```python
sig_handler(sig, frame)
```

Signal handler for SIGINT (Ctrl+C). Exits the program with status code 1. 


---

<a href="../spider.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_arguments`

```python
parse_arguments()
```

Parse command line arguments. 



**Returns:**
 argparse.Namespace: The parsed arguments. 


---

<a href="../spider.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `url_parser`

```python
url_parser(url)
```

Parse and validate the URL. 



**Parameters:**
 
- url (str): The URL to be parsed. 



**Returns:**
 int: 1 if the URL is valid, 0 otherwise. 


---

<a href="../spider.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_images_urls`

```python
get_images_urls(site_url)
```

Retrieve image URLs from the specified site URL. 



**Parameters:**
 
- site_url (str): The URL of the site to be scraped. 



**Returns:**
 list: List of image URLs. 



**Raises:**
 
- requests.exceptions.Timeout: If the request times out. 
- requests.exceptions.HTTPError: If an HTTP error occurs. 
- requests.exceptions.RequestException: If a general request exception occurs. 
- requests.exceptions.ConnectionError: If a connection error occurs. 


---

<a href="../spider.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_images`

```python
download_images(img_urls, data_path, site_url)
```

Download images from the provided URLs. 



**Parameters:**
 
- img_urls (list): List of image URLs. 
- data_path (str): Path where the images will be saved. 
- site_url (str): The base URL of the site. 



**Returns:**
 None 



**Raises:**
 
- requests.RequestException: If an error occurs during image download. 


---

<a href="../spider.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `spider`

```python
spider(site_url, data_path, recursivity_level)
```

Perform web scraping of images recursively. 



**Parameters:**
 
- site_url (str): The URL of the site to be scraped. 
- data_path (str): Path where the images will be saved. 
- recursivity_level (int): Depth level for recursive download. 



**Returns:**
 None 



**Raises:**
 
- sys.exit(1): If the URL is invalid. 


---

<a href="../spider.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `display_header`

```python
display_header()
```

Display the header content. 



**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
