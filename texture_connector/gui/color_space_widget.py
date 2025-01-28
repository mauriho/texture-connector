"""
========================================================================================
Name: color_space_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 01-27-2025

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui

import maya.cmds as cmds

from functools import partial


class ColorSpaceWidget(QtWidgets.QWidget):
    color_space_changed = QtCore.Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setMinimumWidth(100)

        self.color_spaces = {}

        self._create_widgets()
        self._create_layouts()
        self._create_connections()
        self._get_color_spaces()

    def _create_widgets(self) -> None:
        combo_box = QtWidgets.QComboBox()
        size = combo_box.sizeHint().height()

        self.label_push_button = QtWidgets.QPushButton()
        self.label_push_button.setFixedHeight(size)
        self.label_push_button.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )
        self.label_palette = self.label_push_button.palette()

        self.icon_push_button = QtWidgets.QPushButton()
        self.icon_push_button.setFixedSize(size, size)
        self.icon_push_button.setIcon(QtGui.QIcon(":teDownArrow.png"))
        self.icon_palette = self.icon_push_button.palette()

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.label_push_button)
        main_layout.addWidget(self.icon_push_button)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

    def _create_connections(self) -> None:
        self.label_push_button.clicked.connect(self._show_menu)
        self.icon_push_button.clicked.connect(self._show_menu)

    def _show_menu(self):
        menu = QtWidgets.QMenu(self)

        for family in self.color_spaces:
            if family == "Roles":
                continue

            submenu = QtWidgets.QMenu(family)
            menu.addMenu(submenu)

            for color_space in self.color_spaces[family]:
                action = submenu.addAction(color_space)
                action.triggered.connect(partial(self.set_color_space, color_space))

        menu.exec_(QtGui.QCursor.pos())

        self.label_push_button.update()
        self.icon_push_button.update()

    def _get_color_spaces(self) -> None:
        self.color_spaces.clear()

        color_spaces = cmds.colorManagementFileRules(colorSpaceNames=True, query=True)

        for color_space in color_spaces:
            color_space_family = cmds.colorManagementFileRules(
                colorSpaceFamilies=color_space, query=True
            )

            if color_space_family:
                color_space_family = color_space_family[0]

                family_color_spaces = self.color_spaces.get(color_space_family, [])
                family_color_spaces.append(color_space)

                self.color_spaces[color_space_family] = family_color_spaces

    def _update_widget_color(self) -> None:
        color_spaces = cmds.colorManagementFileRules(colorSpaceNames=True, query=True)
        color_space = self.get_color_space()

        if color_space in color_spaces:
            self.label_push_button.setPalette(self.label_palette)
            self.icon_push_button.setPalette(self.icon_palette)
        else:
            label_palette = self.label_push_button.palette()
            icon_palette = self.icon_push_button.palette()

            button_color = QtGui.QColor(QtCore.Qt.red)
            text_color = QtGui.QColor(QtCore.Qt.black)

            label_palette.setColor(QtGui.QPalette.Button, button_color)
            label_palette.setColor(QtGui.QPalette.ButtonText, text_color)
            icon_palette.setColor(QtGui.QPalette.Button, button_color)

            self.label_push_button.setPalette(label_palette)
            self.icon_push_button.setPalette(icon_palette)

    def get_color_space(self) -> str:
        return self.label_push_button.text()

    def set_color_space(self, color_space: str) -> None:
        self.label_push_button.setText(color_space)

        self._update_widget_color()

        self.color_space_changed.emit(color_space)

    def update_color_spaces(self) -> None:
        self._update_widget_color()
        self._get_color_spaces()
