from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

class WelcomeWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to OpenPoster Beta")
        self.setFixedSize(700, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top: icon and title
        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 50, 0, 0)
        icon = QIcon(":/assets/openposter.png")
        icon_label = QLabel()
        pixmap = icon.pixmap(QSize(128, 128))
        icon_label.setPixmap(pixmap)
        title_label = QLabel("Welcome to OpenPoster")
        title_font = title_label.font()
        title_font.setPointSize(30)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Version number label
        version_label = QLabel("v0.0.3")
        version_font = version_label.font()
        version_font.setPointSize(12)
        version_label.setFont(version_font)
        version_label.setStyleSheet("color: #666666;")
        
        top_layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        top_layout.addWidget(title_label, alignment=Qt.AlignHCenter)
        top_layout.addWidget(version_label, alignment=Qt.AlignHCenter)
        top_widget.setLayout(top_layout)
        layout.addWidget(top_widget, stretch=3)

        # Bottom: buttons
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)
        bottom_layout.setSpacing(20)
        btn_new = QPushButton("Create New .ca File")
        btn_open = QPushButton("Open .ca File")
        btn_new.setFixedSize(600, 50)
        btn_open.setFixedSize(600, 50)
        bottom_layout.addWidget(btn_new)
        bottom_layout.addWidget(btn_open)
        bottom_widget.setLayout(bottom_layout)
        layout.addWidget(bottom_widget, stretch=2)

        self.setLayout(layout)

        btn_new.clicked.connect(self.on_new)
        btn_open.clicked.connect(self.on_open)
        self.result = None

    def on_new(self):
        self.result = ("new", None)
        self.accept()

    def on_open(self):
        self.result = ("open", None)
        self.accept()