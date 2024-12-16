"""
========================================================================================
Name: render_plugins.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from enum import Enum


class RenderPlugins(Enum):
    ARNOLD = ("Arnold", "mtoa")
    REDSHIFT = ("Redshift", "redshift4maya")
    V_RAY = ("V-Ray", "vrayformaya")
