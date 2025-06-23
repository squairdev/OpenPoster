from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpinBox, QFormLayout, QWidget, QAbstractSpinBox
from PySide6.QtCore import Qt
import os
import xml.etree.ElementTree as ET

class NewFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New File")
        self.setModal(True)
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()
        # Top: title centered
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 0)
        top_layout.addStretch()
        title_lbl = QLabel("New .ca File")
        title_font = title_lbl.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_lbl.setFont(title_font)
        top_layout.addWidget(title_lbl)
        top_layout.addStretch()
        top_widget.setLayout(top_layout)
        layout.addWidget(top_widget)

        form = QFormLayout()
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'openposter.ca'))
        default_name = os.path.basename(template_dir).replace('.ca', '')
        self.name_edit = QLineEdit(default_name)
        self.name_edit.setStyleSheet("QLineEdit { padding: 4px; border: 1px solid palette(midlight); border-radius: 4px; }")
        form.addRow("File Name:", self.name_edit)

        self.width_spin = QSpinBox()
        self.width_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.width_spin.setRange(1, 10000)
        self.width_spin.setStyleSheet("QSpinBox { padding: 4px; border: 1px solid palette(midlight); border-radius: 4px; }")
        self.height_spin = QSpinBox()
        self.height_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.height_spin.setRange(1, 10000)
        self.height_spin.setStyleSheet("QSpinBox { padding: 4px; border: 1px solid palette(midlight); border-radius: 4px; }")
        try:
            caml_path = os.path.join(template_dir, 'main.caml')
            tree = ET.parse(caml_path)
            root = tree.getroot()
            layer_elem = root.find('{http://www.apple.com/CoreAnimation/1.0}CALayer')
            if layer_elem is not None and layer_elem.get('bounds'):
                parts = layer_elem.get('bounds').split()
                self.width_spin.setValue(int(float(parts[2])))
                self.height_spin.setValue(int(float(parts[3])))
            else:
                self.width_spin.setValue(1170)
                self.height_spin.setValue(2532)
        except:
            self.width_spin.setValue(1170)
            self.height_spin.setValue(2532)
        form.addRow("Width:", self.width_spin)
        form.addRow("Height:", self.height_spin)

        # Center the form layout horizontally
        layout.addLayout(form)
        layout.setAlignment(form, Qt.AlignHCenter)

        # Bottom: back and create buttons
        btn_widget = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 0, 10, 10)
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.on_back)
        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.on_create)
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(create_btn)
        btn_widget.setLayout(btn_layout)
        layout.addWidget(btn_widget)

        self.setLayout(layout)
        self.result = None

    def on_back(self):
        self.result = ("back", None)
        self.accept()

    def on_create(self):
        name = self.name_edit.text().strip()
        width = self.width_spin.value()
        height = self.height_spin.value()
        self.result = ("create", {"name": name, "width": width, "height": height})
        self.accept() 