"""
========================================================================================
Name: texture_connector_settings_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-17-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from __future__ import annotations

try:
    from PySide6 import QtWidgets
    from PySide6 import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore

import maya.api.OpenMaya as om
import maya.cmds as cmds

from texture_connector.gui.material_texture_map_settings_widget import MaterialTextureMapSettingsWidget
from texture_connector.gui.texture_map_settings_widget import TextureMapSettingsWidget
from texture_connector.config import RenderPlugins
from texture_connector.config import UVTilingModes
from texture_connector.config import TextureMaps
from texture_connector.config import ColorSpaces
import texture_connector.utils as utils


class TextureConnectorSettingsWidget(QtWidgets.QWidget):
    PREFERENCES_PATH = utils.get_preferences_path()

    def __init__(self) -> None:
        super().__init__()

        self.call_backs = []

        self.material_texture_map_settings_widget = None
        self.base_color_settings_widget = None
        self.roughness_settings_widget = None
        self.metalness_settings_widget = None
        self.normal_settings_widget = None
        self.height_settings_widget = None
        self.emissive_settings_widget = None
        self.opacity_settings_widget = None
        self.use_triplanar_check_box = None

        self._create_widgets()
        self._create_layouts()
        self._set_render_engines()
        self.load_settings(TextureConnectorSettingsWidget.PREFERENCES_PATH)

    def _create_widgets(self) -> None:
        self.render_engine_combo_box = QtWidgets.QComboBox()
        self.render_engine_combo_box.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )

        self.material_texture_map_settings_widget = MaterialTextureMapSettingsWidget()
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

        self.uv_tiling_mode_combo_box = QtWidgets.QComboBox()
        self.uv_tiling_mode_combo_box.addItems(
            [
                UVTilingModes.OFF,
                UVTilingModes.ZBRUSH,
                UVTilingModes.MUDBOX,
                UVTilingModes.MARI,
            ]
        )
        self.uv_tiling_mode_combo_box.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )

        self.use_triplanar_check_box = QtWidgets.QCheckBox("Use Triplanar")

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(3)

        render_engine_group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(render_engine_group_box)

        render_engine_form_layout = QtWidgets.QFormLayout()
        render_engine_form_layout.addRow(
            "Render Engine: ", self.render_engine_combo_box
        )
        render_engine_form_layout.setContentsMargins(43, 3, 3, 3)
        render_engine_form_layout.setSpacing(3)
        render_engine_group_box.setLayout(render_engine_form_layout)

        main_layout.addWidget(self.material_texture_map_settings_widget)

        uv_tiling_mode_group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(uv_tiling_mode_group_box)

        uv_tiling_mode_form_layout = QtWidgets.QFormLayout()
        uv_tiling_mode_form_layout.addRow(
            "UV Tiling Mode: ", self.uv_tiling_mode_combo_box
        )
        uv_tiling_mode_form_layout.setContentsMargins(39, 3, 3, 3)
        uv_tiling_mode_form_layout.setSpacing(3)
        uv_tiling_mode_group_box.setLayout(uv_tiling_mode_form_layout)

        triplanar_group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(triplanar_group_box)

        triplanar_form_layout = QtWidgets.QFormLayout()
        triplanar_form_layout.addWidget(self.use_triplanar_check_box)
        triplanar_form_layout.setContentsMargins(127, 3, 3, 3)
        triplanar_form_layout.setSpacing(3)
        triplanar_group_box.setLayout(triplanar_form_layout)

    def create_call_backs(self) -> None:
        utils.Logger.debug(f"Callbacks before creating {self.call_backs}.")

        if not self.call_backs:
            self.call_backs.append(
                om.MSceneMessage.addStringArrayCallback(
                    om.MSceneMessage.kAfterPluginLoad, self._set_render_engines
                )
            )

            self.call_backs.append(
                om.MSceneMessage.addStringArrayCallback(
                    om.MSceneMessage.kAfterPluginUnload, self._set_render_engines
                )
            )

        utils.Logger.debug(f"Callbacks after creating {self.call_backs}.")

    def delete_call_backs(self) -> None:
        utils.Logger.debug(f"Callbacks before deleting {self.call_backs}.")

        if self.call_backs:
            for call_back in self.call_backs:
                om.MSceneMessage.removeCallback(call_back)

            self.call_backs.clear()

        utils.Logger.debug(f"Callbacks after deleting {self.call_backs}.")

    def _set_render_engines(self, *args) -> None:
        plugins_loaded = cmds.pluginInfo(listPlugins=True, query=True)

        current_render_engine = self.render_engine_combo_box.currentText()
        self.render_engine_combo_box.clear()

        for plugin in RenderPlugins:
            plugin_name, plugin = plugin.value

            if plugin in plugins_loaded:
                self.render_engine_combo_box.addItem(plugin_name)

        if current_render_engine:
            self.render_engine_combo_box.setCurrentText(current_render_engine)

    def load_settings(self, settings_path: str = "") -> None:
        s = QtCore.QSettings(settings_path, QtCore.QSettings.IniFormat)

        s.beginGroup("settings")

        self.base_color_settings_widget.set_enabled(
            s.value("baseColorEnabled", True, bool)
        )
        self.base_color_settings_widget.set_text(
            s.value("baseColorSuffix", TextureMaps.BASE_COLOR, str)
        )
        self.base_color_settings_widget.set_color_space(
            s.value("baseColorColorSpace", ColorSpaces.SRGB.value, str)
        )

        self.roughness_settings_widget.set_enabled(
            s.value("roughnessEnabled", True, bool)
        )
        self.roughness_settings_widget.set_text(
            s.value("roughnessSuffix", TextureMaps.ROUGHNESS, str)
        )
        self.roughness_settings_widget.set_color_space(
            s.value("roughnessColorSpace", ColorSpaces.RAW.value, str)
        )

        self.metalness_settings_widget.set_enabled(
            s.value("metalnessEnabled", True, bool)
        )
        self.metalness_settings_widget.set_text(
            s.value("metalnessSuffix", TextureMaps.METALNESS, str)
        )
        self.metalness_settings_widget.set_color_space(
            s.value("metalnessColorSpace", ColorSpaces.RAW.value, str)
        )

        self.normal_settings_widget.set_enabled(s.value("normalEnabled", True, bool))
        self.normal_settings_widget.set_text(
            s.value("normalSuffix", TextureMaps.NORMAL, str)
        )
        self.normal_settings_widget.set_color_space(
            s.value("normalColorSpace", ColorSpaces.RAW.value, str)
        )

        self.height_settings_widget.set_enabled(s.value("heightEnabled", True, bool))
        self.height_settings_widget.set_text(
            s.value("heightSuffix", TextureMaps.HEIGHT, str)
        )
        self.height_settings_widget.set_color_space(
            s.value("heightColorSpace", ColorSpaces.RAW.value, str)
        )

        self.emissive_settings_widget.set_enabled(
            s.value("emissiveEnabled", True, bool)
        )
        self.emissive_settings_widget.set_text(
            s.value("emissiveSuffix", TextureMaps.EMISSIVE, str)
        )
        self.emissive_settings_widget.set_color_space(
            s.value("emissiveColorSpace", ColorSpaces.SRGB.value, str)
        )

        self.opacity_settings_widget.set_enabled(s.value("opacityEnabled", True, bool))
        self.opacity_settings_widget.set_text(
            s.value("opacitySuffix", TextureMaps.OPACITY, str)
        )
        self.opacity_settings_widget.set_color_space(
            s.value("opacityColorSpace", ColorSpaces.RAW.value, str)
        )

        self.uv_tiling_mode_combo_box.setCurrentText(
            str(s.value("uvTilingMode", UVTilingModes.OFF, str))
        )

        self.use_triplanar_check_box.setChecked(s.value("useTriplanar", False, bool))

        s.endGroup()

    def save_settings(self) -> None:
        s = QtCore.QSettings(
            TextureConnectorSettingsWidget.PREFERENCES_PATH, QtCore.QSettings.IniFormat
        )

        s.beginGroup("settings")

        s.setValue("baseColorEnabled", self.base_color_settings_widget.is_enabled())
        s.setValue("baseColorSuffix", self.base_color_settings_widget.get_text())
        s.setValue(
            "baseColorColorSpace", self.base_color_settings_widget.get_color_space()
        )

        s.setValue("roughnessEnabled", self.roughness_settings_widget.is_enabled())
        s.setValue("roughnessSuffix", self.roughness_settings_widget.get_text())
        s.setValue(
            "roughnessColorSpace", self.roughness_settings_widget.get_color_space()
        )

        s.setValue("metalnessEnabled", self.metalness_settings_widget.is_enabled())
        s.setValue("metalnessSuffix", self.metalness_settings_widget.get_text())
        s.setValue(
            "metalnessColorSpace", self.metalness_settings_widget.get_color_space()
        )

        s.setValue("normalEnabled", self.normal_settings_widget.is_enabled())
        s.setValue("normalSuffix", self.normal_settings_widget.get_text())
        s.setValue("normalColorSpace", self.normal_settings_widget.get_color_space())

        s.setValue("heightEnabled", self.height_settings_widget.is_enabled())
        s.setValue("heightSuffix", self.height_settings_widget.get_text())
        s.setValue("heightColorSpace", self.height_settings_widget.get_color_space())

        s.setValue("emissiveEnabled", self.emissive_settings_widget.is_enabled())
        s.setValue("emissiveSuffix", self.emissive_settings_widget.get_text())
        s.setValue(
            "emissiveColorSpace", self.emissive_settings_widget.get_color_space()
        )

        s.setValue("opacityEnabled", self.opacity_settings_widget.is_enabled())
        s.setValue("opacitySuffix", self.opacity_settings_widget.get_text())
        s.setValue("opacityColorSpace", self.opacity_settings_widget.get_color_space())

        s.setValue("uvTilingMode", self.uv_tiling_mode_combo_box.currentText())

        s.setValue("useTriplanar", self.use_triplanar_check_box.isChecked())

        s.endGroup()

    def get_render_engine(self) -> str:
        return self.render_engine_combo_box.currentText()

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

    def is_use_triplanar_checked(self) -> bool:
        return self.use_triplanar_check_box.isChecked()

    def get_texture_maps_color_space(self) -> tuple[tuple[str, str], ...]:
        texture_maps_color_space = (
            (TextureMaps.BASE_COLOR, self.base_color_settings_widget.get_color_space()),
            (TextureMaps.ROUGHNESS, self.roughness_settings_widget.get_color_space()),
            (TextureMaps.METALNESS, self.metalness_settings_widget.get_color_space()),
            (TextureMaps.NORMAL, self.normal_settings_widget.get_color_space()),
            (TextureMaps.HEIGHT, self.height_settings_widget.get_color_space()),
            (TextureMaps.EMISSIVE, self.emissive_settings_widget.get_color_space()),
            (TextureMaps.OPACITY, self.opacity_settings_widget.get_color_space()),
        )

        return texture_maps_color_space

    def get_texture_maps_enabled(self) -> tuple[tuple[str, bool], ...]:
        texture_maps_enabled = (
            (TextureMaps.BASE_COLOR, self.base_color_settings_widget.is_enabled()),
            (TextureMaps.ROUGHNESS, self.roughness_settings_widget.is_enabled()),
            (TextureMaps.METALNESS, self.metalness_settings_widget.is_enabled()),
            (TextureMaps.NORMAL, self.normal_settings_widget.is_enabled()),
            (TextureMaps.HEIGHT, self.height_settings_widget.is_enabled()),
            (TextureMaps.EMISSIVE, self.emissive_settings_widget.is_enabled()),
            (TextureMaps.OPACITY, self.opacity_settings_widget.is_enabled()),
        )

        return texture_maps_enabled

    def get_texture_maps_suffix(self) -> tuple[tuple[str, str], ...]:
        texture_maps_suffix = (
            (TextureMaps.BASE_COLOR, self.base_color_settings_widget.get_text()),
            (TextureMaps.ROUGHNESS, self.roughness_settings_widget.get_text()),
            (TextureMaps.METALNESS, self.metalness_settings_widget.get_text()),
            (TextureMaps.NORMAL, self.normal_settings_widget.get_text()),
            (TextureMaps.HEIGHT, self.height_settings_widget.get_text()),
            (TextureMaps.EMISSIVE, self.emissive_settings_widget.get_text()),
            (TextureMaps.OPACITY, self.opacity_settings_widget.get_text()),
        )

        return texture_maps_suffix

    def get_uv_tiling_mode(self) -> str:
        return self.uv_tiling_mode_combo_box.currentText()
