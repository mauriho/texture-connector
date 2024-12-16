"""
========================================================================================
Name: material_settings_list_widget.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-15-2024

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

from collections import defaultdict
import pathlib
import glob
import re

from texture_connector.gui.material_settings_widget import MaterialSettingsWidget
import texture_connector.config as config
import texture_connector.utils as utils


class MaterialSettingsListWidget(QtWidgets.QWidget):
    directory_changed = QtCore.Signal()
    update_clicked = QtCore.Signal()

    def __init__(self) -> None:
        super().__init__()

        self.preferences_path = utils.get_preferences_path()

        self.search_files_in_subdirectories = True
        self.auto_update_on_file_changes = False

        self.image_extensions = tuple(
            [color_space.value for color_space in config.ImageExtensions]
        )
        self.folder_path = ""
        self.texture_maps_suffix = ()

        self.file_system_watcher = QtCore.QFileSystemWatcher()

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    def _create_widgets(self) -> None:
        self.search_material_line_edit = QtWidgets.QLineEdit()
        self.search_material_line_edit.setPlaceholderText("Search...")

        self.unselect_all_materials_push_button = QtWidgets.QPushButton("Unselect All")

        self.select_all_materials_push_button = QtWidgets.QPushButton("Select All")

        self.update_materials_push_button = QtWidgets.QPushButton("Update Materials")

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.search_material_line_edit)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(3)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        self.material_list_items_widget = QtWidgets.QWidget()
        self.material_list_items_widget.setProperty("localStyle", True)
        self.material_list_items_widget.setStyleSheet(
            "QWidget[localStyle='true'] {background-color: rgb(40, 40, 40);}"
        )
        scroll_area.setWidget(self.material_list_items_widget)

        self.material_list_items_v_box_layout = QtWidgets.QVBoxLayout()
        self.material_list_items_v_box_layout.setAlignment(QtCore.Qt.AlignTop)
        self.material_list_items_v_box_layout.setContentsMargins(3, 3, 3, 3)
        self.material_list_items_v_box_layout.setSpacing(3)
        self.material_list_items_widget.setLayout(self.material_list_items_v_box_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.unselect_all_materials_push_button)
        layout.addWidget(self.select_all_materials_push_button)

        main_layout.addLayout(layout)
        main_layout.addWidget(self.update_materials_push_button)

    def _create_connections(self) -> None:
        self.file_system_watcher.directoryChanged.connect(
            self._directory_changed_file_system_watcher
        )

        self.search_material_line_edit.textChanged.connect(
            self._search_material_text_changed_line_edit
        )
        self.unselect_all_materials_push_button.clicked.connect(
            self._unselect_all_clicked_action
        )
        self.select_all_materials_push_button.clicked.connect(
            self._select_all_clicked_action
        )
        self.update_materials_push_button.clicked.connect(
            self._update_materials_clicked_push_button
        )

    def _directory_changed_file_system_watcher(self) -> None:
        self._load_preferences()

        if self.auto_update_on_file_changes:
            self.directory_changed.emit()

    def _search_material_text_changed_line_edit(self, text: str) -> None:
        text_lower = text.lower()

        for material_settings_widget in self.get_material_settings_widgets():
            if text_lower in material_settings_widget.get_material_name().lower():
                material_settings_widget.setVisible(True)
            else:
                material_settings_widget.setVisible(False)

    def _unselect_all_clicked_action(self) -> None:
        for material_settings_widget in self.get_material_settings_widgets():
            material_settings_widget.set_enabled(False)

    def _select_all_clicked_action(self) -> None:
        for material_settings_widget in self.get_material_settings_widgets():
            material_settings_widget.set_enabled(True)

    def _update_materials_clicked_push_button(self) -> None:
        self.update_clicked.emit()

    def _add_directory_and_subdirectories(self, folder_path):
        self.file_system_watcher.addPath(folder_path)

        q_dir = QtCore.QDir(folder_path)
        subfolders = q_dir.entryList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)

        for subfolder in subfolders:
            self._add_directory_and_subdirectories(q_dir.filePath(subfolder))

    def _load_preferences(self) -> None:
        s = QtCore.QSettings(self.preferences_path, QtCore.QSettings.IniFormat)

        s.beginGroup("preferences")

        self.search_files_in_subdirectories = s.value(
            "searchFilesInSubdirectories", True, bool
        )
        self.auto_update_on_file_changes = s.value(
            "autoUpdateMaterialsOnFolderChanges", False, bool
        )

        s.endGroup()

    def _get_material_texture_paths(
        self,
    ) -> dict[str, list[tuple[str, str]]]:

        materials = defaultdict(list)

        if self.search_files_in_subdirectories:
            files = glob.glob(f"{self.folder_path}/**/*", recursive=True)
        else:
            files = glob.glob(f"{self.folder_path}/*")

        files.sort(reverse=True)

        for file_path in files:
            path = pathlib.Path(file_path)
            path_suffix = path.suffix

            if path_suffix in self.image_extensions:
                for texture_map_name, texture_map_suffix in self.texture_maps_suffix:
                    if texture_map_suffix:
                        material_name = self._get_material_name_from_texture_map_path(
                            path=path, texture_map_suffix=texture_map_suffix
                        )

                        if material_name:
                            materials[material_name].append(
                                (texture_map_name, file_path)
                            )

        return dict(materials)

    @staticmethod
    def _get_material_name_from_texture_map_path(
        path: pathlib.Path, texture_map_suffix: str
    ) -> str:
        pattern = rf"(.+?)(?=_{texture_map_suffix})(?=_.*$|$)"
        match = re.search(pattern, path.stem, re.IGNORECASE)

        if match:
            return match.group(1)
        else:
            return ""

    def clear_material_settings_widgets(self) -> None:
        for material_settings_widget in self.get_material_settings_widgets():
            material_settings_widget.deleteLater()

    def create_material_settings_widgets(self) -> None:
        self._load_preferences()
        self.clear_material_settings_widgets()

        material_texture_paths = self._get_material_texture_paths()

        for material_name, textures_paths in material_texture_paths.items():
            material_widget = MaterialSettingsWidget()
            material_widget.set_material_name(material_name)
            self.material_list_items_v_box_layout.addWidget(material_widget)

            for texture_type, texture_path in textures_paths:
                texture_path_short_name = utils.remove_prefix(
                    prefix=self.folder_path, string=texture_path
                )

                if texture_type == config.TextureMaps.BASE_COLOR:
                    base_color_widget = material_widget.get_base_color_settings_widget()
                    base_color_widget.set_path(texture_path)
                    base_color_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.ROUGHNESS:
                    roughness_widget = material_widget.get_roughness_settings_widget()
                    roughness_widget.set_path(texture_path)
                    roughness_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.METALNESS:
                    metalness_widget = material_widget.get_metalness_settings_widget()
                    metalness_widget.set_path(texture_path)
                    metalness_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.NORMAL:
                    normal_widget = material_widget.get_normal_settings_widget()
                    normal_widget.set_path(texture_path)
                    normal_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.HEIGHT:
                    height_widget = material_widget.get_height_settings_widget()
                    height_widget.set_path(texture_path)
                    height_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.EMISSIVE:
                    emissive_widget = material_widget.get_emissive_settings_widget()
                    emissive_widget.set_path(texture_path)
                    emissive_widget.set_text(texture_path_short_name)

                if texture_type == config.TextureMaps.OPACITY:
                    opacity_widget = material_widget.get_opacity_settings_widget()
                    opacity_widget.set_path(texture_path)
                    opacity_widget.set_text(texture_path_short_name)

        self._search_material_text_changed_line_edit(
            self.search_material_line_edit.text()
        )

    def get_material_settings_widgets(self) -> list[MaterialSettingsWidget]:
        material_settings_widgets = []

        for child in self.material_list_items_widget.children():
            if isinstance(child, MaterialSettingsWidget):
                material_settings_widgets.append(child)

        return material_settings_widgets

    def set_folder_path(self, folder_path: str) -> None:
        self._load_preferences()

        self.folder_path = folder_path

        file_system_watcher_directories = self.file_system_watcher.directories()

        if file_system_watcher_directories:
            self.file_system_watcher.removePaths(file_system_watcher_directories)

        if self.search_files_in_subdirectories:
            self._add_directory_and_subdirectories(self.folder_path)
        else:
            self.file_system_watcher.addPath(self.folder_path)

    def set_texture_maps_suffix(
        self, texture_maps_suffix: tuple[tuple[str, str], ...]
    ) -> None:
        self.texture_maps_suffix = texture_maps_suffix

    def set_base_color_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            base_color_widget = material_widget.get_base_color_settings_widget()
            base_color_widget.set_color_space(color_space)

    def set_base_color_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            base_color_widget = material_widget.get_base_color_settings_widget()
            base_color_widget.setVisible(enabled)

    def set_roughness_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            roughness_widget = material_widget.get_roughness_settings_widget()
            roughness_widget.set_color_space(color_space)

    def set_roughness_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            roughness_widget = material_widget.get_roughness_settings_widget()
            roughness_widget.setVisible(enabled)

    def set_metalness_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            metalness_widget = material_widget.get_metalness_settings_widget()
            metalness_widget.set_color_space(color_space)

    def set_metalness_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            metalness_widget = material_widget.get_metalness_settings_widget()
            metalness_widget.setVisible(enabled)

    def set_normal_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            normal_widget = material_widget.get_normal_settings_widget()
            normal_widget.set_color_space(color_space)

    def set_normal_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            normal_widget = material_widget.get_normal_settings_widget()
            normal_widget.setVisible(enabled)

    def set_height_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            height_widget = material_widget.get_height_settings_widget()
            height_widget.set_color_space(color_space)

    def set_height_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            height_widget = material_widget.get_height_settings_widget()
            height_widget.setVisible(enabled)

    def set_emissive_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            emissive_widget = material_widget.get_emissive_settings_widget()
            emissive_widget.set_color_space(color_space)

    def set_emissive_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            emissive_widget = material_widget.get_emissive_settings_widget()
            emissive_widget.setVisible(enabled)

    def set_opacity_widgets_color_space(self, color_space: str) -> None:
        for material_widget in self.get_material_settings_widgets():
            opacity_widget = material_widget.get_opacity_settings_widget()
            opacity_widget.set_color_space(color_space)

    def set_opacity_widgets_enabled(self, enabled: bool) -> None:
        for material_widget in self.get_material_settings_widgets():
            opacity_widget = material_widget.get_opacity_settings_widget()
            opacity_widget.setVisible(enabled)

    def set_texture_map_widgets_color_space(
        self, widgets_color_space: tuple[tuple[str, str], ...]
    ) -> None:
        for texture_map_type, color_space in widgets_color_space:
            if texture_map_type == config.TextureMaps.BASE_COLOR:
                self.set_base_color_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.ROUGHNESS:
                self.set_roughness_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.METALNESS:
                self.set_metalness_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.NORMAL:
                self.set_normal_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.HEIGHT:
                self.set_height_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.EMISSIVE:
                self.set_emissive_widgets_color_space(color_space)

            if texture_map_type == config.TextureMaps.OPACITY:
                self.set_opacity_widgets_color_space(color_space)

    def set_texture_map_widgets_enabled(
        self, widgets_enabled: tuple[tuple[str, bool], ...]
    ) -> None:
        for texture_map_type, enabled in widgets_enabled:
            if texture_map_type == config.TextureMaps.BASE_COLOR:
                self.set_base_color_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.ROUGHNESS:
                self.set_roughness_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.METALNESS:
                self.set_metalness_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.NORMAL:
                self.set_normal_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.HEIGHT:
                self.set_height_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.EMISSIVE:
                self.set_emissive_widgets_enabled(enabled)

            if texture_map_type == config.TextureMaps.OPACITY:
                self.set_opacity_widgets_enabled(enabled)
