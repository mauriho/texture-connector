"""
========================================================================================
Name: texture_map_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from PySide2 import QtWidgets

import sys

from texture_connector.gui.texture_map_settings_widget import TextureMapSettingsWidget


def main():
    app = QtWidgets.QApplication(sys.argv)

    texture_settings_widget = TextureMapSettingsWidget()
    texture_settings_widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
