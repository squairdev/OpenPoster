from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QToolButton, QLabel
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QSize
from ui.ui_export_options_dialog import Ui_ExportOptionsDialog

class ExportOptionsDialog(QDialog):
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.choice = None
        self.config_manager = config_manager
        self.parent = parent

        self.ui = Ui_ExportOptionsDialog()
        self.ui.setupUi(self)

        # Add close shortcut for the dialog itself
        if self.config_manager:
            close_shortcut_str = self.config_manager.get_close_window_shortcut()
            if close_shortcut_str:
                self.close_shortcut = QShortcut(QKeySequence(close_shortcut_str), self)
                self.close_shortcut.activated.connect(self.close)

        # Dynamic properties and signal connections
        # Base styling for titleLabel, buttons is in .ui

        self.ui.copyButton.clicked.connect(lambda: self.set_choice("copy"))
        self.ui.tendiesButton.clicked.connect(lambda: self.set_choice("tendies"))
        self.ui.nuggetButton.clicked.connect(lambda: self.set_choice("nugget"))

        if parent and hasattr(parent, 'ca_files_in_tendies') and len(getattr(parent, 'ca_files_in_tendies', [])) > 1:
            self.ui.copyButton.setText("Export as .ca files in folder")
        
        is_dark = False
        if parent and hasattr(parent, 'isDarkMode'):
            is_dark = parent.isDarkMode
            
            if is_dark:
                self.ui.copyButton.setIcon(QIcon(":/icons/export-white.svg"))
                self.ui.tendiesButton.setIcon(QIcon(":/icons/export-white.svg"))
                nugget_icon_path = ":/icons/nugget-export-white.png" if is_dark else ":/icons/nugget-export.png"
                self.ui.nuggetButton.setIcon(QIcon(nugget_icon_path))
                
                self.ui.titleLabel.setStyleSheet("font-size:18px; font-weight:bold; color: #FFFFFF;")
                self.ui.copyButton.setStyleSheet("QToolButton { color: #FFFFFF; background-color: #3A3A3A; border: 1px solid #606060; border-radius: 8px; }")
                self.ui.tendiesButton.setStyleSheet("QToolButton { color: #FFFFFF; background-color: #3A3A3A; border: 1px solid #606060; border-radius: 8px; }")
                self.ui.nuggetButton.setStyleSheet("QToolButton { color: #FFFFFF; background-color: #3A3A3A; border: 1px solid #606060; border-radius: 8px; }")
            else:
                self.ui.copyButton.setIcon(QIcon(":/icons/export.svg"))
                self.ui.tendiesButton.setIcon(QIcon(":/icons/export.svg"))
                nugget_icon_path = ":/icons/nugget-export.png"
                self.ui.nuggetButton.setIcon(QIcon(nugget_icon_path))

                self.ui.titleLabel.setStyleSheet("font-size:18px; font-weight:bold; color: #303030;")
                self.ui.copyButton.setStyleSheet("QToolButton { color: #303030; background-color: #F0F0F0; border: 1px solid #A0A0A0; border-radius: 8px; }")
                self.ui.tendiesButton.setStyleSheet("QToolButton { color: #303030; background-color: #F0F0F0; border: 1px solid #A0A0A0; border-radius: 8px; }")
                self.ui.nuggetButton.setStyleSheet("QToolButton { color: #303030; background-color: #F0F0F0; border: 1px solid #A0A0A0; border-radius: 8px; }")

    def set_choice(self, choice):
        self.choice = choice
        self.accept() 