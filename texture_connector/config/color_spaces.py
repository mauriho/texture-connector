"""
========================================================================================
Name: color_spaces.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.

https://help.autodesk.com/view/MAYAUL/2025/ENU/?guid=GUID-2622A6C2-B79B-442E-B5C3-327474409CC7
========================================================================================
"""

from enum import Enum


class ColorSpaces(Enum):
    SRGB = "sRGB"
    ACESCG = "ACEScg"
    RAW = "Raw"
