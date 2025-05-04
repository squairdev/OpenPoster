from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QToolButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

class ExportOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.choice = None
        self.setModal(True)
        self.setWindowTitle("Export Options")
        self.resize(500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("How would you like to export?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(title)
        options_layout = QHBoxLayout()
        options_layout.setContentsMargins(0, 20, 0, 0)
        border_color = "#fff" if getattr(self.parent(), 'isDarkMode', False) else "#000"
        size = 180
        icon_size = QSize(64, 64)
        copy_btn = QToolButton(self)
        copy_btn.setIcon(QIcon(":/icons/export-white.svg") if getattr(self.parent(), 'isDarkMode', False) else QIcon(":/icons/export.svg"))
        copy_btn.setIconSize(icon_size)
        copy_btn.setText("Export as a copy")
        copy_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        copy_btn.setFixedSize(size, size)
        copy_btn.setStyleSheet(f"border:1px solid {border_color};border-radius:15px;")
        copy_btn.clicked.connect(lambda: self.select('copy'))
        options_layout.addWidget(copy_btn)
        tendies_btn = QToolButton(self)
        tendies_btn.setIcon(QIcon(":/icons/export-white.svg") if getattr(self.parent(), 'isDarkMode', False) else QIcon(":/icons/export.svg"))
        tendies_btn.setIconSize(icon_size)
        tendies_btn.setText("Export as .tendies")
        tendies_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tendies_btn.setFixedSize(size, size)
        tendies_btn.setStyleSheet(f"border:1px solid {border_color};border-radius:15px;")
        tendies_btn.clicked.connect(lambda: self.select('tendies'))
        options_layout.addWidget(tendies_btn)
        nugget_btn = QToolButton(self)
        nugget_btn.setIcon(QIcon(":/assets/nugget.png"))
        nugget_btn.setIconSize(icon_size)
        nugget_btn.setText("Export to Nugget")
        nugget_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        nugget_btn.setFixedSize(size, size)
        nugget_btn.setStyleSheet(f"border:1px solid {border_color};border-radius:15px;")
        nugget_btn.clicked.connect(lambda: self.select('nugget'))
        options_layout.addWidget(nugget_btn)
        layout.addLayout(options_layout)

    def select(self, choice):
        self.choice = choice
        self.accept() 