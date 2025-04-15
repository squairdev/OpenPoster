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
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
)
from PySide6.QtGui import (
    QIcon,
)
import os
import sys
import xml.etree.ElementTree as et
import xml.dom.minidom as minidom

from micasa import XmlGenerator as XmlGen
from micasa import AnimationObjectEditor as AnimEdit

# app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Micasa test ui")
        self.setFixedSize(QSize(600, 480))
        self.XmlGen = XmlGen()
        self.AnimEdit = AnimEdit()
        self._object_saved = None
        self._file_path = None

        self.base_path = os.path.dirname(__file__)
        self.icon_path = os.path.abspath(os.path.join(self.base_path, "..", "..", "assets", "openposter.ico"))

        if os.path.exists(self.icon_path):
            self.app_icon = QIcon(self.icon_path)
            self.setWindowIcon(self.app_icon)
        else:
            print("skipping icon")
        
        central_widget = QWidget(self)
        main_layout = QVBoxLayout()

        # for these input and whatever ONLY
        mx_group = QGroupBox("XML Export Settings")
        mx_group_layout = QVBoxLayout()

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

        # make xml inputs
        self.mxinput_startframe = QLineEdit(self)
        self.mxinput_startframe.setPlaceholderText("Starting frame number (Required e.g. 0 or 1)")
        mx_group_layout.addWidget(self.mxinput_startframe)

        self.mxinput_endframe = QLineEdit(self)
        self.mxinput_endframe.setPlaceholderText("Ending frame number (Required)")
        mx_group_layout.addWidget(self.mxinput_endframe)

        self.mxinput_fileprefix = QLineEdit(self)
        self.mxinput_fileprefix.setPlaceholderText("File prefix (e.g. FrameID_ if you have one)")
        mx_group_layout.addWidget(self.mxinput_fileprefix)

        self.mxinput_fileextension = QLineEdit(self)
        self.mxinput_fileextension.setPlaceholderText("File extension (Required. e.g. .png, .jpg)")
        mx_group_layout.addWidget(self.mxinput_fileextension)

        self.mxinput_padding = QLineEdit(self)
        self.mxinput_padding.setPlaceholderText("Padding (Required. e.g. 0001 will be 4)")
        mx_group_layout.addWidget(self.mxinput_padding)

        self.mxinput_fps = QLineEdit(self)
        self.mxinput_fps.setPlaceholderText("FPS (Required. e.g. 24, 30, 60)")
        mx_group_layout.addWidget(self.mxinput_fps)

        self.mxinput_step = QLineEdit(self)
        self.mxinput_step.setPlaceholderText("Step/Frame skip (Required. e.g. 1, 2)")
        mx_group_layout.addWidget(self.mxinput_step)

        self.mxinput_button_hbox = QHBoxLayout()
        self.mxinput_button_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.mxinput_exportasanimation = QCheckBox("Export as animation object")
        self.mxinput_button_hbox.addWidget(self.mxinput_exportasanimation)

        self.mxinput_withroot = QCheckBox("Include <root> tag")
        self.mxinput_button_hbox.addWidget(self.mxinput_withroot)

        mx_group_layout.addLayout(self.mxinput_button_hbox)

        # layout first
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # add mx box
        mx_group.setLayout(mx_group_layout)
        mx_group.setFixedSize(550, 300)
        main_layout.addWidget(mx_group, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        # make xml commands
        self.mx_generate_button = QPushButton("Save to memory", self)
        self.mx_generate_button.setFixedSize(150, 30)
        button_layout.addWidget(self.mx_generate_button)

        self.mx_preview_button = QPushButton("Preview", self)
        self.mx_preview_button.setFixedSize(150, 30)
        button_layout.addWidget(self.mx_preview_button)

        # GEN/PREVIEW FUNC
        self.mx_generate_button.clicked.connect(lambda: self.previewXmlData(True))
        self.mx_preview_button.clicked.connect(lambda: self.previewXmlData(False))

        mx_group_layout.addLayout(button_layout)

        # injector menu
        inject_group = QGroupBox("Direct Inject (Requires export as animation and no root)")
        inject_group_layout = QVBoxLayout()

        self.inject_targettype = QLineEdit(self)
        self.inject_targettype.setPlaceholderText("Target type (Required e.g. CALayer)")
        inject_group_layout.addWidget(self.inject_targettype)

        self.inject_targetattr = QLineEdit(self)
        self.inject_targetattr.setPlaceholderText("Target attribute (Required e.g. name, nuggetId)")
        inject_group_layout.addWidget(self.inject_targetattr)

        self.inject_targetname = QLineEdit(self)
        self.inject_targetname.setPlaceholderText("Target name/id (Required e.g. Layer1, 2)")
        inject_group_layout.addWidget(self.inject_targetname)

        inject_button_layout = QHBoxLayout()
        inject_button_layout.addStretch()

        self.inject_button = QPushButton("INJECT (Just put the main.caml file in this directory for this demo)", self)
        self.inject_button.setFixedSize(400, 30)
        inject_button_layout.addWidget(self.inject_button)

        # INJECT FUNC
        self.inject_button.clicked.connect(lambda: self.injectObject())

        inject_group_layout.addLayout(inject_button_layout)

        # injector box
        inject_group.setLayout(inject_group_layout)
        inject_group.setFixedSize(550, 150)
        main_layout.addWidget(inject_group, alignment=Qt.AlignmentFlag.AlignCenter)

        # finalize
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # checking and stuff
    def previewXmlData(self, save_to_memory):
        start_frame = self.mxinput_startframe.text()
        end_frame = self.mxinput_endframe.text()
        file_prefix = self.mxinput_fileprefix.text()
        file_extension = self.mxinput_fileextension.text()
        padding = self.mxinput_padding.text()
        fps = self.mxinput_fps.text()
        step = self.mxinput_step.text()
        export_as_animation = self.mxinput_exportasanimation.isChecked()
        with_root = self.mxinput_withroot.isChecked()

        # int check for everything
        def toInt(value, name):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    raise ValueError(f"{name} is not an int/float ({value})")
            
        try:
            start_frame = toInt(start_frame, "sf")
            end_frame = toInt(end_frame, "ef")
            padding = toInt(padding, "pad")
            fps = toInt(fps, "fps")
            step = toInt(step, "step")
        except ValueError as e:
            print(e)
            return

        data = self.XmlGen.make_xml(
            startFrame=start_frame,
            endFrame=end_frame,
            filePrefix=file_prefix,
            fileExtension=file_extension,
            padding=padding,
            exportAsAnimation=export_as_animation,
            fps=fps,
            step=step,
            withRoot=with_root
        )

        if save_to_memory:
            self._object_saved = data
            print(save_to_memory)
            return
        
        xml_str = et.tostring(data.getroot(), 'utf-8')
        formatted = minidom.parseString(xml_str).toprettyxml("\t")
        print(formatted)

    # injecting func call
    def injectObject(self):
        type = self.inject_targettype.text()
        attr = self.inject_targetattr.text()
        name = self.inject_targetname.text()

        if not type:
            print("Missing type")
            return
        if not attr:
            print("Missing attribute")
            return
        if not name:
            print("Missing name")
            return
        if not self._object_saved:
            print("no saved object in memory")
            return

        self.AnimEdit.load_file("main.caml")
        self.AnimEdit.insert_object_to_target(type, attr, name, self._object_saved.getroot())
        self.AnimEdit.save_file("main_output.caml")


# central loader
class MWLoader():
    def __init__(self):
        mw_app = QApplication(sys.argv)
        mw_ui = MainWindow()
        mw_ui.show()
        mw_app.exec()


if __name__ == "__main__":
    MWLoader()