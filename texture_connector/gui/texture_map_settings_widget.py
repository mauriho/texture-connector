"""
========================================================================================
Name: texture_map_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 01-10-2025

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore

from texture_connector.gui.color_space_widget import ColorSpaceWidget


class TextureMapSettingsWidget(QtWidgets.QWidget):
    color_space_changed = QtCore.Signal(str)
    enable_toggled = QtCore.Signal(bool)

    def __init__(self) -> None:
        super().__init__()

        self.path = ""

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self) -> None:
        self.enable_check_box = QtWidgets.QCheckBox()

        self.title_label = QtWidgets.QLabel()
        self.title_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.title_label.setFixedWidth(100)

        self.text_line_edit = QtWidgets.QLineEdit()

        self.color_spaces_widget = ColorSpaceWidget()

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.enable_check_box)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)

        self.frame = QtWidgets.QFrame()
        self.frame.setEnabled(False)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )
        main_layout.addWidget(self.frame)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.text_line_edit)
        layout.addWidget(self.color_spaces_widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(3)
        self.frame.setLayout(layout)

    def _create_connections(self) -> None:
        self.enable_check_box.toggled.connect(self._enabled_toggled_check_box)
        self.color_spaces_widget.color_space_changed.connect(
            self._color_spaces_color_space_changed_combo_box
        )

    def _enabled_toggled_check_box(self, checked: bool) -> None:
        self.frame.setEnabled(checked)

        self.enable_toggled.emit(checked)

    def _color_spaces_color_space_changed_combo_box(self, text: str) -> None:
        self.color_space_changed.emit(text)

    def is_enabled(self) -> bool:
        return self.enable_check_box.isChecked()

    def get_color_space(self) -> str:
        return self.color_spaces_widget.get_color_space()

    def get_path(self) -> str:
        return self.path

    def get_text(self) -> str:
        return self.text_line_edit.text()

    def set_color_space(self, color_space: str) -> None:
        self.color_spaces_widget.set_color_space(color_space)

    def set_color_spaces_visible(self, enabled: bool) -> None:
        self.color_spaces_widget.setVisible(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.enable_check_box.setChecked(enabled)

    def set_path(self, path: str) -> None:
        self.path = path

    def set_read_only(self) -> None:
        self.text_line_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.text_line_edit.setReadOnly(True)

    def set_text(self, text: str) -> None:
        text = text.replace("\\", "/")
        self.text_line_edit.setText(text)

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def update_color_spaces(self) -> None:
        self.color_spaces_widget.update_color_spaces()
