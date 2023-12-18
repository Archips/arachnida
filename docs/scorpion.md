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
- **BOLD**
- **GREEN**
- **WARNING**
- **END**
- **EXIF_MEMBER**
- **HEADER**

---

<a href="../scorpion.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sig_handler`

```python
sig_handler(sig, frame)
```

Signal handler for SIGINT (Ctrl+C). Exits the program with status code 1. 


---

<a href="../scorpion.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_arguments`

```python
parse_arguments()
```






---

<a href="../scorpion.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `basic_metadata`

```python
basic_metadata(image, image_members)
```






---

<a href="../scorpion.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `date_time_exif`

```python
date_time_exif(image, image_members)
```






---

<a href="../scorpion.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_dms_coordinates`

```python
format_dms_coordinates(coordinates)
```






---

<a href="../scorpion.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dms_coordinates_to_dd_coordinates`

```python
dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref)
```






---

<a href="../scorpion.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `draw_map_for_location`

```python
draw_map_for_location(latitude, latitude_ref, longitude, longitude_ref)
```






---

<a href="../scorpion.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `geo_location_exif`

```python
geo_location_exif(image, image_members)
```






---

<a href="../scorpion.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `device_exif`

```python
device_exif(image, image_members)
```






---

<a href="../scorpion.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `lens_exif`

```python
lens_exif(image, image_members)
```






---

<a href="../scorpion.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `scorpion`

```python
scorpion(img_path)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
