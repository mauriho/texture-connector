"""
========================================================================================================================
Name: uv_tiling_modes.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-08-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.

https://help.autodesk.com/view/MAYAUL/2025/ENU/?guid=GUID-132520C0-F1DF-4C74-B8C1-D89154ADFBDB
========================================================================================================================
"""


class UVTilingModes:
    OFF = 'Off'
    ZBRUSH = '0-based (ZBrush)'  # u0_v0
    MUDBOX = '1-based (MudBox)'  # u1_v1
    MARI = 'UDIM (Mari)'         # 1000+(u+1+v*10)
