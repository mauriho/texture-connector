"""
========================================================================================================================
Name: material_texture_map_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-11-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
"""
try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore

from texture_connector.gui.texture_map_settings_widget import TextureMapSettingsWidget


class MaterialTextureMapSettingsWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._create_widgets()
        self._create_layouts()

    def _create_widgets(self) -> None:
        self.base_color_texture_map_settings_widget = TextureMapSettingsWidget()
        self.base_color_texture_map_settings_widget.set_enabled(True)
        self.base_color_texture_map_settings_widget.set_title('Base Color: ')

        self.roughness_texture_map_settings_widget = TextureMapSettingsWidget()
        self.roughness_texture_map_settings_widget.set_enabled(True)
        self.roughness_texture_map_settings_widget.set_title('Roughness: ')

        self.metalness_texture_map_settings_widget = TextureMapSettingsWidget()
        self.metalness_texture_map_settings_widget.set_enabled(True)
        self.metalness_texture_map_settings_widget.set_title('Metalness: ')

        self.normal_texture_map_settings_widget = TextureMapSettingsWidget()
        self.normal_texture_map_settings_widget.set_enabled(True)
        self.normal_texture_map_settings_widget.set_title('Normal: ')

        self.height_texture_map_settings_widget = TextureMapSettingsWidget()
        self.height_texture_map_settings_widget.set_enabled(True)
        self.height_texture_map_settings_widget.set_title('Height: ')

        self.emissive_texture_map_settings_widget = TextureMapSettingsWidget()
        self.emissive_texture_map_settings_widget.set_enabled(True)
        self.emissive_texture_map_settings_widget.set_title('Emissive: ')

        self.opacity_texture_map_settings_widget = TextureMapSettingsWidget()
        self.opacity_texture_map_settings_widget.set_enabled(True)
        self.opacity_texture_map_settings_widget.set_title('Opacity: ')

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(QtCore.QMargins())

        group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(group_box)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.base_color_texture_map_settings_widget)
        layout.addWidget(self.roughness_texture_map_settings_widget)
        layout.addWidget(self.metalness_texture_map_settings_widget)
        layout.addWidget(self.normal_texture_map_settings_widget)
        layout.addWidget(self.height_texture_map_settings_widget)
        layout.addWidget(self.emissive_texture_map_settings_widget)
        layout.addWidget(self.opacity_texture_map_settings_widget)
        layout.setContentsMargins(QtCore.QMargins(3, 3, 3, 3))
        layout.setSpacing(3)
        group_box.setLayout(layout)

    def get_base_color_settings_widget(self) -> TextureMapSettingsWidget:
        return self.base_color_texture_map_settings_widget

    def get_roughness_settings_widget(self) -> TextureMapSettingsWidget:
        return self.roughness_texture_map_settings_widget

    def get_metalness_settings_widget(self) -> TextureMapSettingsWidget:
        return self.metalness_texture_map_settings_widget

    def get_normal_settings_widget(self) -> TextureMapSettingsWidget:
        return self.normal_texture_map_settings_widget

    def get_height_settings_widget(self) -> TextureMapSettingsWidget:
        return self.height_texture_map_settings_widget

    def get_emissive_settings_widget(self) -> TextureMapSettingsWidget:
        return self.emissive_texture_map_settings_widget

    def get_opacity_settings_widget(self) -> TextureMapSettingsWidget:
        return self.opacity_texture_map_settings_widget

    def set_read_only(self) -> None:
        self.base_color_texture_map_settings_widget.set_read_only()
        self.roughness_texture_map_settings_widget.set_read_only()
        self.metalness_texture_map_settings_widget.set_read_only()
        self.normal_texture_map_settings_widget.set_read_only()
        self.height_texture_map_settings_widget.set_read_only()
        self.emissive_texture_map_settings_widget.set_read_only()
        self.opacity_texture_map_settings_widget.set_read_only()
