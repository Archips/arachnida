<!-- markdownlint-disable -->

<a href="../scorpion.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `scorpion.py`
scorpion.py - A script to extract metadata and Exif data from images. 

Usage:  scorpion.py IMG [IMG ...] 

Options:  IMG         Path(s) to the image file(s). 

Description:  This script takes one or more image file paths as input and extracts metadata  as well as Exif data from each image. The extracted information includes  basic details such as filename, image format, size, height, width, mode,  palette, animation status, and the number of frames. Additionally, it extracts  Exif data if available. 

Dependencies: 
    - Python 3 
    - Pillow (PIL) library for image processing 

**Global Variables**
---------------
- **TAGS**
- **BOLD**
- **GREEN**
- **WARNING**
- **END**
- **HEADER**

---

<a href="../scorpion.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sig_handler`

```python
sig_handler(sig, frame)
```






---

<a href="../scorpion.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_arguments`

```python
parse_arguments()
```






---

<a href="../scorpion.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_metadata`

```python
extract_metadata(image)
```






---

<a href="../scorpion.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_exif`

```python
extract_exif(image)
```






---

<a href="../scorpion.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `scorpion`

```python
scorpion(img)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
