"""
========================================================================================================================
Name: texture_connector_ui.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
from PySide2 import QtWidgets

import sys

from texture_connector.gui.texture_connector_ui import TextureConnectorUI


def main():
    app = QtWidgets.QApplication(sys.argv)

    texture_settings_widget = TextureConnectorUI()
    texture_settings_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
