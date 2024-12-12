"""
========================================================================================================================
Name: preferences_ui.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-12-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================================================
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
    WINDOW_NAME = 'textureConnectorPreferences'
    WINDOW_TITLE = 'Preferences'

    save_clicked = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.preferences_path = utils.get_preferences_path()

        self.resize(400, 200)
        self.setObjectName(PreferencesUI.WINDOW_NAME)
        self.setWindowTitle(PreferencesUI.WINDOW_TITLE)
        self.setModal(True)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_preferences()

    def _create_widgets(self) -> None:
        self.search_files_in_subdirectories_check_box = QtWidgets.QCheckBox('Search Files in Subdirectories')
        self.auto_update_on_file_changes_check_box = QtWidgets.QCheckBox('Auto Update on File Changes')

        self.save_push_button = QtWidgets.QPushButton('Save')

        self.cancel_push_button = QtWidgets.QPushButton('Cancel')

    def _create_layouts(self) -> None:
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setContentsMargins(QtCore.QMargins())
        main_layout.setSpacing(3)

        group_box = QtWidgets.QGroupBox()
        main_layout.addWidget(group_box)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addWidget(self.search_files_in_subdirectories_check_box)
        form_layout.addWidget(self.auto_update_on_file_changes_check_box)
        form_layout.setContentsMargins(QtCore.QMargins(3, 3, 3, 3))
        form_layout.setSpacing(3)
        group_box.setLayout(form_layout)

        h_box_layout = QtWidgets.QHBoxLayout()
        h_box_layout.addWidget(self.save_push_button)
        h_box_layout.addWidget(self.cancel_push_button)
        main_layout.addStretch()
        main_layout.addLayout(h_box_layout)

    def _create_connections(self) -> None:
        self.save_push_button.clicked.connect(self._save_clicked_push_button)
        self.cancel_push_button.clicked.connect(self.close)

    def _save_clicked_push_button(self) -> None:
        self._save_preferences()
        self.close()

        self.save_clicked.emit()

    def _load_preferences(self) -> None:
        s = QtCore.QSettings(self.preferences_path, QtCore.QSettings.IniFormat)

        s.beginGroup('preferences')
        self.search_files_in_subdirectories_check_box.setChecked(s.value('searchFilesInSubdirectories', True, bool))
        self.auto_update_on_file_changes_check_box.setChecked(s.value('autoUpdateOnFileChanges', False, bool))
        s.endGroup()

    def _save_preferences(self) -> None:
        s = QtCore.QSettings(self.preferences_path, QtCore.QSettings.IniFormat)

        s.beginGroup('preferences')
        s.setValue('searchFilesInSubdirectories', self.search_files_in_subdirectories_check_box.isChecked())
        s.setValue('autoUpdateOnFileChanges', self.auto_update_on_file_changes_check_box.isChecked())
        s.endGroup()
