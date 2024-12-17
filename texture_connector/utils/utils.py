"""
========================================================================================
Name: __init__.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-16-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from maya.api.OpenMaya import MGlobal
import maya.cmds as cmds

import sys
import os


def display_error(message: str) -> None:
    MGlobal.displayError(f"[Texture Connector] {message}")


def display_info(message: str) -> None:
    MGlobal.displayInfo(f"[Texture Connector] {message}")


def display_warning(message: str) -> None:
    MGlobal.displayWarning(f"[Texture Connector] {message}")


def get_preferences_path() -> str:
    user_pref_dir = cmds.internalVar(userPrefDir=True)
    preferences_path = os.path.join(
        user_pref_dir, "textureConnector", "textureConnectorPreferences.ini"
    )

    return preferences_path


def get_settings_path() -> str:
    user_pref_dir = cmds.internalVar(userPrefDir=True)
    settings_path = os.path.join(
        user_pref_dir, "textureConnector", "textureConnectorSettings.ini"
    )

    return settings_path


def remove_prefix(prefix: str, string: str) -> str:
    if string:
        if sys.version_info >= (3, 9):
            return string.removeprefix(prefix)
        elif string.startswith(prefix):
            return string[len(prefix):]

    return string
