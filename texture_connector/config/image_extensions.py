"""
========================================================================================================================
Name: image_extensions.py
Author: Mauricio Gonzalez Soto
Updated Date: 11-24-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.

https://help.autodesk.com/view/MAYAUL/2025/ENU/?guid=GUID-0182C713-D891-41EF-915A-4A5E61E1CBE3
========================================================================================================================
"""
from enum import Enum


class ImageExtensions(Enum):
    GIF = '.gif'
    JPEG = '.jpg'
    PNG = '.png'
    OPEN_EXR = '.exr'
    TIFF = '.tif'
