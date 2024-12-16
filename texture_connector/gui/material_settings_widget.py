"""
========================================================================================
Name: material_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore

from texture_connector.gui.material_texture_map_settings_widget import MaterialTextureMapSettingsWidget
from texture_connector.gui.texture_map_settings_widget import TextureMapSettingsWidget


class MaterialSettingsWidget(QtWidgets.QWidget):
    enable_toggled = QtCore.Signal(bool)

    def __init__(self) -> None:
        super().__init__()

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self) -> None:
        self.enable_check_box = QtWidgets.QCheckBox()
        self.enable_check_box.setChecked(True)

        self.title_label = QtWidgets.QLabel("Material: ")
        self.title_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.title_label.setFixedWidth(80)

        self.text_line_edit = QtWidgets.QLineEdit()

        self.material_texture_map_settings_widget = MaterialTextureMapSettingsWidget()
        self.material_texture_map_settings_widget.set_read_only()

        self.base_color_settings_widget = (
            self.material_texture_map_settings_widget.get_base_color_settings_widget()
        )
        self.roughness_settings_widget = (
            self.material_texture_map_settings_widget.get_roughness_settings_widget()
        )
        self.metalness_settings_widget = (
            self.material_texture_map_settings_widget.get_metalness_settings_widget()
        )
        self.normal_settings_widget = (
            self.material_texture_map_settings_widget.get_normal_settings_widget()
        )
        self.height_settings_widget = (
            self.material_texture_map_settings_widget.get_height_settings_widget()
        )
        self.emissive_settings_widget = (
            self.material_texture_map_settings_widget.get_emissive_settings_widget()
        )
        self.opacity_settings_widget = (
            self.material_texture_map_settings_widget.get_opacity_settings_widget()
        )

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(3)

        group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(group_box)

        material_main_h_box_layout = QtWidgets.QHBoxLayout()
        material_main_h_box_layout.addWidget(self.enable_check_box)
        material_main_h_box_layout.setContentsMargins(3, 3, 3, 3)
        material_main_h_box_layout.setSpacing(6)
        group_box.setLayout(material_main_h_box_layout)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )
        material_main_h_box_layout.addWidget(self.frame)

        material_h_box_layout = QtWidgets.QHBoxLayout()
        material_h_box_layout.addWidget(self.title_label)
        material_h_box_layout.addWidget(self.text_line_edit)
        material_h_box_layout.setContentsMargins(3, 3, 3, 3)
        material_h_box_layout.setSpacing(3)
        self.frame.setLayout(material_h_box_layout)

        material_texture_map_settings_v_box_layout = QtWidgets.QVBoxLayout()
        material_texture_map_settings_v_box_layout.addWidget(
            self.material_texture_map_settings_widget
        )
        material_texture_map_settings_v_box_layout.setContentsMargins(12, 0, 0, 0)
        main_layout.addLayout(material_texture_map_settings_v_box_layout)

    def _create_connections(self) -> None:
        self.enable_check_box.toggled.connect(self._enabled_toggled_check_box)

    def _enabled_toggled_check_box(self, checked: bool) -> None:
        self.frame.setEnabled(checked)
        self.material_texture_map_settings_widget.setVisible(checked)

        self.enable_toggled.emit(checked)

    def is_enabled(self) -> bool:
        return self.enable_check_box.isChecked()

    def get_material_name(self) -> str:
        return self.text_line_edit.text()

    def get_base_color_settings_widget(self) -> TextureMapSettingsWidget:
        return self.base_color_settings_widget

    def get_roughness_settings_widget(self) -> TextureMapSettingsWidget:
        return self.roughness_settings_widget

    def get_metalness_settings_widget(self) -> TextureMapSettingsWidget:
        return self.metalness_settings_widget

    def get_normal_settings_widget(self) -> TextureMapSettingsWidget:
        return self.normal_settings_widget

    def get_height_settings_widget(self) -> TextureMapSettingsWidget:
        return self.height_settings_widget

    def get_emissive_settings_widget(self) -> TextureMapSettingsWidget:
        return self.emissive_settings_widget

    def get_opacity_settings_widget(self) -> TextureMapSettingsWidget:
        return self.opacity_settings_widget

    def set_enabled(self, enabled: bool) -> None:
        self.enable_check_box.setChecked(enabled)

    def set_material_name(self, name: str) -> None:
        self.text_line_edit.setText(name)
