from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PySide6.QtGui import (
    QIcon,
)
import os
import sys

from micasa import XmlGenerator

# app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Micasa test ui")
        self.setFixedSize(QSize(800, 600))

        self.base_path = os.path.dirname(__file__)
        self.icon_path = os.path.abspath(os.path.join(self.base_path, "..", "..", "assets", "openposter.ico"))

        if os.path.exists(self.icon_path):
            self.app_icon = QIcon(self.icon_path)
            self.setWindowIcon(self.app_icon)
        else:
            print("skipping icon")
        
        central_widget = QWidget(self)
        layout = QVBoxLayout()

        #make_xml(
        #    self,
        #    startFrame = 0,
        #    endFrame = 1,
        #    filePrefix = '',
        #    fileExtension = '.png',
        #    padding = 4,
        #    exportAsAnimation = False,
        #    fps = 30,
        #    withRoot = True
        #):

        self.mxinput_startframe = QLineEdit(self)
        self.mxinput_startframe.setPlaceholderText("Starting frame number")
        layout.addWidget(self.mxinput_startframe)

        self.mxinput_endframe = QLineEdit(self)
        self.mxinput_endframe.setPlaceholderText("Ending frame number")
        layout.addWidget(self.mxinput_endframe)

        self.mxinput_fileprefix = QLineEdit(self)
        self.mxinput_fileprefix.setPlaceholderText("File prefix (e.g. FrameID_ if you have one)")
        layout.addWidget(self.mxinput_fileprefix)

        self.mxinput_fileextension = QLineEdit(self)
        self.mxinput_fileextension.setPlaceholderText("File extension (e.g. .png, .jpg)")
        layout.addWidget(self.mxinput_fileextension)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


# central loader
class MWLoader():
    def __init__(self):
        mw_app = QApplication(sys.argv)
        mw_ui = MainWindow()
        mw_ui.show()
        mw_app.exec()


if __name__ == "__main__":
    MWLoader()