"""
========================================================================================
Name: texture_connector_ui.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-17-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

try:
    from shiboken6 import wrapInstance
    from PySide6 import QtWidgets
    from PySide6 import QtCore
    from PySide6 import QtGui
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui

from maya.OpenMayaUI import MQtUtil
from maya import cmds

import webbrowser
import os

from texture_connector.gui.texture_connector_settings_widget import TextureConnectorSettingsWidget
from texture_connector.gui.material_settings_list_widget import MaterialSettingsListWidget
from texture_connector.gui.material_settings_widget import MaterialSettingsWidget
from texture_connector.gui.preferences_ui import PreferencesUI
from texture_connector.core import CreateMaterialNetworkRedshift
from texture_connector.core import CreateMaterialNetworkArnold
from texture_connector.core import CreateMaterialNetworkVRay
from texture_connector.core import CreateMaterialNetwork
from texture_connector.config import RenderPlugins
import texture_connector.utils as utils


class TextureConnectorUI(QtWidgets.QDialog):
    WINDOW_NAME = "textureConnector"
    WINDOW_TITLE = "Texture Connector"

    PREFERENCES_PATH = utils.get_preferences_path()

    dialog_instance = None

    @classmethod
    def display(cls) -> None:
        if not cls.dialog_instance:
            cls.dialog_instance = TextureConnectorUI()

        if cls.dialog_instance.isHidden():
            cls.dialog_instance.show()
        else:
            cls.dialog_instance.raise_()
            cls.dialog_instance.activateWindow()

    @classmethod
    def maya_main_window(cls) -> QtWidgets.QWidget:
        main_window_ptr = MQtUtil.mainWindow()
        main_window = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

        return main_window

    def __init__(self) -> None:
        super().__init__(self.maya_main_window())

        self.geometry = None

        self.preferences_ui = PreferencesUI(self)
        self.auto_set_project_source_images_folder = False

        self.resize(800, 600)
        self.setObjectName(TextureConnectorUI.WINDOW_NAME)
        self.setWindowTitle(TextureConnectorUI.WINDOW_TITLE)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self) -> None:
        self.menu_bar = QtWidgets.QMenuBar()

        edit_menu = self.menu_bar.addMenu("Edit")
        edit_menu.addAction("Save Settings", self._save_settings)
        edit_menu.addAction("Reset Settings", self._reset_settings)
        edit_menu.addSeparator()
        edit_menu.addAction("Preferences", self._open_preferences)

        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("Help on Texture Connector", self._open_help)

        self.folder_path_line_edit = QtWidgets.QLineEdit()
        self.folder_path_line_edit.setPlaceholderText("Select a folder...")

        push_button_size = self.folder_path_line_edit.sizeHint().height()

        self.select_folder_path_push_button = QtWidgets.QPushButton("...")
        self.select_folder_path_push_button.setFixedSize(
            QtCore.QSize(push_button_size, push_button_size)
        )

        self.texture_connector_settings_widget = TextureConnectorSettingsWidget()

        self.base_color_settings_widget = (
            self.texture_connector_settings_widget.get_base_color_settings_widget()
        )
        self.roughness_settings_widget = (
            self.texture_connector_settings_widget.get_roughness_settings_widget()
        )
        self.metalness_settings_widget = (
            self.texture_connector_settings_widget.get_metalness_settings_widget()
        )
        self.normal_settings_widget = (
            self.texture_connector_settings_widget.get_normal_settings_widget()
        )
        self.height_settings_widget = (
            self.texture_connector_settings_widget.get_height_settings_widget()
        )
        self.emissive_settings_widget = (
            self.texture_connector_settings_widget.get_emissive_settings_widget()
        )
        self.opacity_settings_widget = (
            self.texture_connector_settings_widget.get_opacity_settings_widget()
        )

        self.material_settings_list_widget = MaterialSettingsListWidget()

        self.create_materials_push_button = QtWidgets.QPushButton("Create Materials")

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 3, 6, 6)
        main_layout.setMenuBar(self.menu_bar)
        main_layout.setSpacing(3)

        folder_path_h_box_layout = QtWidgets.QHBoxLayout()
        folder_path_h_box_layout.addWidget(self.folder_path_line_edit)
        folder_path_h_box_layout.addWidget(self.select_folder_path_push_button)
        folder_path_h_box_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(folder_path_h_box_layout)

        splitter = QtWidgets.QSplitter()
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.create_materials_push_button)

        left_widget = QtWidgets.QWidget()
        splitter.addWidget(left_widget)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.texture_connector_settings_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget.setLayout(left_layout)

        right_widget = QtWidgets.QWidget()
        splitter.addWidget(right_widget)
        splitter.setSizes([375, 375])

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.material_settings_list_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget.setLayout(right_layout)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setStretchFactor(1, 1)

    def _create_connections(self) -> None:
        self.folder_path_line_edit.returnPressed.connect(
            self._folder_path_return_pressed_line_edit
        )
        self.select_folder_path_push_button.clicked.connect(
            self._select_folder_path_clicked_push_button
        )

        self.base_color_settings_widget.current_color_space_changed.connect(
            self._base_color_settings_current_color_space_changed_widget
        )
        self.base_color_settings_widget.enable_toggled.connect(
            self._base_color_settings_enable_toggled_widget
        )
        self.roughness_settings_widget.current_color_space_changed.connect(
            self._roughness_settings_current_color_space_changed_widget
        )
        self.roughness_settings_widget.enable_toggled.connect(
            self._roughness_settings_enable_toggled_widget
        )
        self.metalness_settings_widget.current_color_space_changed.connect(
            self._metalness_settings_current_color_space_changed_widget
        )
        self.metalness_settings_widget.enable_toggled.connect(
            self._metalness_settings_enable_toggled_widget
        )
        self.normal_settings_widget.current_color_space_changed.connect(
            self._normal_settings_current_color_space_changed_widget
        )
        self.normal_settings_widget.enable_toggled.connect(
            self._normal_settings_enable_toggled_widget
        )
        self.height_settings_widget.current_color_space_changed.connect(
            self._height_settings_current_color_space_changed_widget
        )
        self.height_settings_widget.enable_toggled.connect(
            self._height_settings_enable_toggled_widget
        )
        self.emissive_settings_widget.current_color_space_changed.connect(
            self._emissive_settings_current_color_space_changed_widget
        )
        self.emissive_settings_widget.enable_toggled.connect(
            self._emissive_settings_enable_toggled_widget
        )
        self.opacity_settings_widget.current_color_space_changed.connect(
            self._opacity_settings_current_color_space_changed_widget
        )
        self.opacity_settings_widget.enable_toggled.connect(
            self._opacity_settings_enable_toggled_widget
        )

        self.material_settings_list_widget.directory_changed.connect(
            self._material_settings_list_directory_changed_widget
        )
        self.material_settings_list_widget.update_clicked.connect(
            self._material_settings_list_update_clicked_widget
        )

        self.create_materials_push_button.clicked.connect(
            self._create_materials_clicked_push_button
        )

        self.preferences_ui.save_clicked.connect(self._preferences_ui_save_clicked)

    def _save_settings(self) -> None:
        self.texture_connector_settings_widget.save_settings()

    def _reset_settings(self) -> None:
        self.texture_connector_settings_widget.load_settings()

    def _open_preferences(self) -> None:
        self.preferences_ui.show()

    @staticmethod
    def _open_help() -> None:
        webbrowser.open("https://github.com/mauriciogonzalezsoto/texture-connector")

    def _load_preferences(self) -> None:
        s = QtCore.QSettings(
            TextureConnectorUI.PREFERENCES_PATH, QtCore.QSettings.IniFormat
        )

        s.beginGroup("preferences")
        self.auto_set_project_source_images_folder = s.value(
            "autoSetProjectSourceImagesFolder", False, bool
        )
        s.endGroup()

    def _folder_path_return_pressed_line_edit(self) -> None:
        folder_path = self.folder_path_line_edit.text()

        if folder_path:
            if os.path.exists(folder_path):
                self.material_settings_list_widget.set_folder_path(folder_path)
                self._create_material_settings_widgets()
            else:
                utils.display_error(f"{folder_path!r} folder does not exist.")
        else:
            self.material_settings_list_widget.clear_material_settings_widgets()

    def _select_folder_path_clicked_push_button(self) -> None:
        current_maya_project_path = cmds.workspace(rootDirectory=True, query=True)
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder", current_maya_project_path
        )

        if folder_path:
            self.folder_path_line_edit.setText(folder_path)
            self.material_settings_list_widget.set_folder_path(folder_path)
            self._create_material_settings_widgets()

    def _base_color_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_base_color_widgets_color_space(
            self.base_color_settings_widget.get_color_space()
        )

    def _base_color_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_base_color_widgets_enabled(
            self.base_color_settings_widget.is_enabled()
        )

    def _roughness_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_roughness_widgets_color_space(
            self.roughness_settings_widget.get_color_space()
        )

    def _roughness_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_roughness_widgets_enabled(
            self.roughness_settings_widget.is_enabled()
        )

    def _metalness_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_metalness_widgets_color_space(
            self.metalness_settings_widget.get_color_space()
        )

    def _metalness_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_metalness_widgets_enabled(
            self.metalness_settings_widget.is_enabled()
        )

    def _normal_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_normal_widgets_color_space(
            self.normal_settings_widget.get_color_space()
        )

    def _normal_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_normal_widgets_enabled(
            self.normal_settings_widget.is_enabled()
        )

    def _height_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_height_widgets_color_space(
            self.height_settings_widget.get_color_space()
        )

    def _height_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_height_widgets_enabled(
            self.height_settings_widget.is_enabled()
        )

    def _emissive_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_emissive_widgets_color_space(
            self.emissive_settings_widget.get_color_space()
        )

    def _emissive_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_emissive_widgets_enabled(
            self.emissive_settings_widget.is_enabled()
        )

    def _opacity_settings_current_color_space_changed_widget(self) -> None:
        self.material_settings_list_widget.set_opacity_widgets_color_space(
            self.opacity_settings_widget.get_color_space()
        )

    def _opacity_settings_enable_toggled_widget(self) -> None:
        self.material_settings_list_widget.set_opacity_widgets_enabled(
            self.opacity_settings_widget.is_enabled()
        )

    def _material_settings_list_directory_changed_widget(self) -> None:
        self._create_material_settings_widgets()

    def _material_settings_list_update_clicked_widget(self) -> None:
        self._create_material_settings_widgets()

    def _create_materials_clicked_push_button(self) -> None:
        render_engine = self.texture_connector_settings_widget.get_render_engine()
        materials = self.material_settings_list_widget.get_material_settings_widgets()
        count = 0

        for material_settings_widget in materials:
            if material_settings_widget.is_enabled():
                if render_engine == RenderPlugins.ARNOLD.value[0]:
                    material_network = CreateMaterialNetworkArnold()
                elif render_engine == RenderPlugins.REDSHIFT.value[0]:
                    material_network = CreateMaterialNetworkRedshift()
                elif render_engine == RenderPlugins.V_RAY.value[0]:
                    material_network = CreateMaterialNetworkVRay()
                else:
                    utils.display_error(
                        "No supported render engine loaded (Arnold, Redshift, V-Ray)."
                    )

                    return

                if material_network:
                    self._create_material_network(
                        material_network=material_network,
                        material_settings_widget=material_settings_widget,
                    )

                    count += 1

        if count:
            utils.display_info(f"{count} material(s) created.")
        else:
            utils.display_warning("No material has been created.")

    def _preferences_ui_save_clicked(self):
        self._folder_path_return_pressed_line_edit()

    def _create_material_network(
        self,
        material_network: CreateMaterialNetwork,
        material_settings_widget: MaterialSettingsWidget,
    ) -> None:
        if self.base_color_settings_widget.is_enabled():
            base_color_widget = (
                material_settings_widget.get_base_color_settings_widget()
            )

            if base_color_widget.is_enabled():
                material_network.set_base_color_settings(
                    color_space=base_color_widget.get_color_space(),
                    file_path=base_color_widget.get_path(),
                    suffix=self.base_color_settings_widget.get_text(),
                )

        if self.roughness_settings_widget.is_enabled():
            roughness_widget = material_settings_widget.get_roughness_settings_widget()

            if roughness_widget.is_enabled():
                material_network.set_roughness_settings(
                    color_space=roughness_widget.get_color_space(),
                    file_path=roughness_widget.get_path(),
                    suffix=self.roughness_settings_widget.get_text(),
                )

        if self.metalness_settings_widget.is_enabled():
            metalness_widget = material_settings_widget.get_metalness_settings_widget()

            if metalness_widget.is_enabled():
                material_network.set_metalness_settings(
                    color_space=metalness_widget.get_color_space(),
                    file_path=metalness_widget.get_path(),
                    suffix=self.metalness_settings_widget.get_text(),
                )

        if self.normal_settings_widget.is_enabled():
            normal_widget = material_settings_widget.get_normal_settings_widget()

            if normal_widget.is_enabled():
                material_network.set_normal_settings(
                    color_space=normal_widget.get_color_space(),
                    file_path=normal_widget.get_path(),
                    suffix=self.normal_settings_widget.get_text(),
                )

        if self.height_settings_widget.is_enabled():
            height_widget = material_settings_widget.get_height_settings_widget()

            if height_widget.is_enabled():
                material_network.set_height_settings(
                    color_space=height_widget.get_color_space(),
                    file_path=height_widget.get_path(),
                    suffix=self.height_settings_widget.get_text(),
                )

        if self.emissive_settings_widget.is_enabled():
            emissive_widget = material_settings_widget.get_emissive_settings_widget()

            if emissive_widget.is_enabled():
                material_network.set_emissive_settings(
                    color_space=emissive_widget.get_color_space(),
                    file_path=emissive_widget.get_path(),
                    suffix=self.emissive_settings_widget.get_text(),
                )

        if self.opacity_settings_widget.is_enabled():
            opacity_widget = material_settings_widget.get_opacity_settings_widget()

            if opacity_widget.is_enabled():
                material_network.set_opacity_settings(
                    color_space=opacity_widget.get_color_space(),
                    file_path=opacity_widget.get_path(),
                    suffix=self.opacity_settings_widget.get_text(),
                )

        triplanar = self.texture_connector_settings_widget.is_use_triplanar_checked()
        uv_tiling_mode = self.texture_connector_settings_widget.get_uv_tiling_mode()

        material_network.create(
            name=material_settings_widget.get_material_name(),
            use_triplanar=triplanar,
            uv_tiling_mode=uv_tiling_mode,
        )

    def _create_material_settings_widgets(self) -> None:
        self.material_settings_list_widget.set_texture_maps_suffix(
            self.texture_connector_settings_widget.get_texture_maps_suffix()
        )

        self.material_settings_list_widget.create_material_settings_widgets()

        self.material_settings_list_widget.set_texture_map_widgets_color_space(
            self.texture_connector_settings_widget.get_texture_maps_color_space()
        )

        self.material_settings_list_widget.set_texture_map_widgets_enabled(
            self.texture_connector_settings_widget.get_texture_maps_enabled()
        )

    def _set_project_source_images_folder(self) -> None:
        current_folder_path = self.folder_path_line_edit.text()

        if self.auto_set_project_source_images_folder and not current_folder_path:
            current_maya_project_path = cmds.workspace(rootDirectory=True, query=True)
            source_images_folder = os.path.join(
                current_maya_project_path, "sourceimages"
            )

            if os.path.exists(source_images_folder):
                self.folder_path_line_edit.setText(source_images_folder)

                self.material_settings_list_widget.set_folder_path(source_images_folder)
                self._create_material_settings_widgets()
            else:
                utils.display_error(f"{source_images_folder!r} folder does not exist.")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if isinstance(self, TextureConnectorUI):
            super().closeEvent(event)

            self.geometry = self.saveGeometry()

        self.material_settings_list_widget.clear_file_system_watcher()
        self.texture_connector_settings_widget.delete_call_backs()

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)

        if self.geometry:
            self.restoreGeometry(self.geometry)

        self.material_settings_list_widget.add_file_system_watcher_paths()
        self.texture_connector_settings_widget.create_call_backs()

        self._load_preferences()
        self._set_project_source_images_folder()
