import sys
import os
from lib.main.main import CAFile
from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMainWindow, QTableWidgetItem
from ui.ui_mainwindow import Ui_OpenPoster


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_OpenPoster()
        self.ui.setupUi(self)
        self.ui.openFile.clicked.connect(self.openFile)
        self.ui.treeWidget.currentItemChanged.connect(self.openInInspector)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Key", "Value"])
        self.ui.filename.mousePressEvent = self.toggleFilenameDisplay
        self.showFullPath = True

    def toggleFilenameDisplay(self, event):
        if hasattr(self, 'cafilepath'):
            if self.showFullPath:
                self.ui.filename.setText(os.path.basename(self.cafilepath))
            else:
                self.ui.filename.setText(self.cafilepath)
            self.showFullPath = not self.showFullPath

    def openFile(self):
        self.ui.treeWidget.clear()
        if sys.platform == "darwin":
            self.cafilepath = QFileDialog.getOpenFileName(
                self, "Select File", "", "Core Animation Files (*.ca)")[0]
        else:
            self.cafilepath = QFileDialog.getExistingDirectory(
                self, "Select Folder", "")
                
        if self.cafilepath:
            self.ui.filename.setText(self.cafilepath)
            self.ui.filename.setStyleSheet("border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px;")
            self.showFullPath = True
            self.cafile = CAFile(self.cafilepath)

            self.ui.treeWidget.addTopLevelItem(
                QTreeWidgetItem([self.cafile.rootlayer.name, "Root", self.cafile.rootlayer.id]))

            if len(self.cafile.rootlayer._sublayerorder) > 0:
                self.treeWidgetChildren(
                    self.ui.treeWidget.topLevelItem(0), self.cafile.rootlayer)
        else:
            self.ui.filename.setText("No File Open")
            self.ui.filename.setStyleSheet("border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px; color: #666666; font-style: italic;")

    def treeWidgetChildren(self, item, layer):
        for id in layer._sublayerorder:
            sublayer = layer.sublayers.get(id)
            item.addChild(QTreeWidgetItem(
                [sublayer.name, "Layer", sublayer.id, layer.id]))

            if len(sublayer._sublayerorder) > 0:
                self.treeWidgetChildren(
                    item.child(item.childCount()-1), sublayer)
            if sublayer._animations is not None:
                print(sublayer.animations)
                for animation in sublayer.animations:
                    print(animation)
                    item.child(item.childCount()-1).addChild(QTreeWidgetItem(
                        [animation.keyPath, "Animation", "", sublayer.id]))

    def openInInspector(self, current, _):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.insertRow(0)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("name"))
        self.ui.tableWidget.item(0, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(current.text(0)))
        print(current.text(0), current.text(1),
              current.text(2), current.text(3))
        if current.text(1) == "Animation":
            # element = self.cafile.root.find(
            #    f".//*[@id='{current.text(3)}']/{{*}}animations/*[@keyPath='{current.text(0)}']")
            parent = self.cafile.rootlayer.findlayer(current.text(3))
            element = parent.findanimation(current.text(0))
        elif current.text(1) == "Layer":
            # element = self.cafile.root.find(
            #    f".//*[@id='{current.text(3)}']/{{*}}sublayers/*[@id='{current.text(2)}']")
            element = self.cafile.rootlayer.findlayer(current.text(2))
        elif current.text(1) == "Root":
            element = self.cafile.rootlayer
        else:
            element = None
            print("erm")
        print(element)
