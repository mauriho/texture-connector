"""
========================================================================================================================
Name: material_settings_list_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-01-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from PySide2 import QtWidgets

import sys

from texture_connector.gui.material_settings_list_widget import MaterialSettingsListWidget
from texture_connector.config import TextureMaps


def main():
    folder_path = ''
    texture_map_suffixes = (
        (TextureMaps.BASE_COLOR, 'basecolor'),
        (TextureMaps.ROUGHNESS, 'roughness'),
        (TextureMaps.METALNESS, 'metalness'),
        (TextureMaps.NORMAL, 'normal'),
        (TextureMaps.HEIGHT, 'height'),
        (TextureMaps.EMISSIVE, 'emissive'),
        (TextureMaps.OPACITY, 'opacity')
    )

    app = QtWidgets.QApplication(sys.argv)

    texture_settings_widget = MaterialSettingsListWidget()
    texture_settings_widget.set_folder_path(folder_path)
    texture_settings_widget.set_texture_map_suffixes(texture_map_suffixes)
    texture_settings_widget.create_material_settings_widgets()
    texture_settings_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
