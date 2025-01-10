"""
========================================================================================
Name: preferences_ui.py
Author: Mauricio Gonzalez Soto
Updated Date: 01-10-2025

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


import texture_connector.utils as utils


class PreferencesUI(QtWidgets.QDialog):
    WINDOW_NAME = "textureConnectorPreferences"
    WINDOW_TITLE = "Preferences"

    PREFERENCES_PATH = utils.get_preferences_path()

    GENERAL = "General"
    COLOR_MANAGEMENT = "Color Management"

    save_clicked = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.resize(600, 400)
        self.setObjectName(PreferencesUI.WINDOW_NAME)
        self.setWindowTitle(PreferencesUI.WINDOW_TITLE)
        self.setModal(True)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_preferences()

    def _create_widgets(self) -> None:
        self.categories_list_widget = QtWidgets.QListWidget()
        self.categories_list_widget.addItems(
            [PreferencesUI.GENERAL, PreferencesUI.COLOR_MANAGEMENT]
        )
        self.categories_list_widget.setCurrentRow(0)
        self.categories_list_widget.setFixedWidth(150)

        self.search_files_in_subdirectories_check_box = QtWidgets.QCheckBox(
            "Search files in subdirectories"
        )
        self.auto_set_project_source_images_folder_check_box = QtWidgets.QCheckBox(
            "Auto-set project sourceimages folder"
        )
        self.use_maya_color_space_rules_check_box = QtWidgets.QCheckBox(
            "Use Maya color space rules"
        )

        self.save_push_button = QtWidgets.QPushButton("Save")

        self.cancel_push_button = QtWidgets.QPushButton("Cancel")

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(3)

        h_box_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(h_box_layout)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.categories_list_widget)
        h_box_layout.addLayout(left_layout)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setAlignment(QtCore.Qt.AlignTop)
        h_box_layout.addLayout(right_layout)

        self.general_group_box = QtWidgets.QGroupBox("Main Window")
        right_layout.addWidget(self.general_group_box)

        general_form_layout = QtWidgets.QFormLayout()
        general_form_layout.addWidget(
            self.auto_set_project_source_images_folder_check_box
        )
        general_form_layout.addWidget(self.search_files_in_subdirectories_check_box)
        general_form_layout.setContentsMargins(3, 3, 3, 3)
        general_form_layout.setSpacing(3)
        self.general_group_box.setLayout(general_form_layout)

        self.color_management_group_box = QtWidgets.QGroupBox("Color Management")
        self.color_management_group_box.setVisible(False)
        right_layout.addWidget(self.color_management_group_box)

        color_management_form_layout = QtWidgets.QFormLayout()
        color_management_form_layout.addWidget(
            self.use_maya_color_space_rules_check_box
        )
        color_management_form_layout.setContentsMargins(3, 3, 3, 3)
        color_management_form_layout.setSpacing(3)
        self.color_management_group_box.setLayout(color_management_form_layout)

        h_box_layout = QtWidgets.QHBoxLayout()
        h_box_layout.addWidget(self.save_push_button)
        h_box_layout.addWidget(self.cancel_push_button)
        main_layout.addLayout(h_box_layout)

    def _create_connections(self) -> None:
        self.categories_list_widget.itemClicked.connect(
            self._categories_item_clicked_list_widget
        )

        self.save_push_button.clicked.connect(self._save_clicked_push_button)
        self.cancel_push_button.clicked.connect(self.close)

    def _categories_item_clicked_list_widget(
        self, item: QtWidgets.QListWidgetItem
    ) -> None:

        self.general_group_box.setVisible(False)
        self.color_management_group_box.setVisible(False)

        category = item.text()

        if category == PreferencesUI.GENERAL:
            self.general_group_box.setVisible(True)
        elif category == PreferencesUI.COLOR_MANAGEMENT:
            self.color_management_group_box.setVisible(True)

    def _save_clicked_push_button(self) -> None:
        self._save_preferences()
        self.close()

        self.save_clicked.emit()

    def _load_preferences(self) -> None:
        s = QtCore.QSettings(PreferencesUI.PREFERENCES_PATH, QtCore.QSettings.IniFormat)

        s.beginGroup("general")
        self.search_files_in_subdirectories_check_box.setChecked(
            bool(s.value("searchFilesInSubdirectories", True, bool))
        )
        self.auto_set_project_source_images_folder_check_box.setChecked(
            bool(s.value("autoSetProjectSourceImagesFolder", False, bool))
        )
        s.endGroup()

        s.beginGroup("colorManagement")
        self.use_maya_color_space_rules_check_box.setChecked(
            bool(s.value("useMayaColorSpaceRules", False, bool))
        )
        s.endGroup()

    def _save_preferences(self) -> None:
        s = QtCore.QSettings(PreferencesUI.PREFERENCES_PATH, QtCore.QSettings.IniFormat)

        s.beginGroup("general")
        s.setValue(
            "searchFilesInSubdirectories",
            self.search_files_in_subdirectories_check_box.isChecked(),
        )
        s.setValue(
            "autoSetProjectSourceImagesFolder",
            self.auto_set_project_source_images_folder_check_box.isChecked(),
        )
        s.endGroup()

        s.beginGroup("colorManagement")
        s.setValue(
            "useMayaColorSpaceRules",
            self.use_maya_color_space_rules_check_box.isChecked(),
        )
        s.endGroup()
