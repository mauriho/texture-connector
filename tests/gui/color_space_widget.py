"""
========================================================================================
Name: color_space_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 01-10-2025

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from PySide2 import QtWidgets

import sys

from texture_connector.gui.color_space_widget import ColorSpaceWidget


def main():
    app = QtWidgets.QApplication(sys.argv)

    color_space_widget = ColorSpaceWidget()
    color_space_widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
