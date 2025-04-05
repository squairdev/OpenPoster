import random
import sys
from lib.main.main import CAFile
from PySide6 import QtCore, QtGui
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

    def openFile(self):
        if sys.platform == "darwin":
            self.cafilepath = QFileDialog.getOpenFileName(self, "Select File", "", "Core Animation Files (*.ca)")[
                0]
        else:
            self.cafilepath = QFileDialog.getExistingDirectory(
                self, "Select Folder", "")[0]
        self.ui.filename.setText(self.cafilepath)
        self.cafile = CAFile(self.cafilepath)

        self.ui.treeWidget.addTopLevelItem(
            QTreeWidgetItem([self.cafile.rootlayer.name, "Root", self.cafile.rootlayer.id]))

        if len(self.cafile.rootlayer._sublayerorder) > 0:
            self.treeWidgetChildren(
                self.ui.treeWidget.topLevelItem(0), self.cafile.rootlayer)

    def treeWidgetChildren(self, item, layer):
        for id in layer._sublayerorder:
            sublayer = layer.sublayers.get(id)
            item.addChild(QTreeWidgetItem(
                [sublayer.name, "Layer", sublayer.id]))

            if len(sublayer._sublayerorder) > 0:
                self.treeWidgetChildren(
                    item.child(item.childCount()-1), sublayer)
            if sublayer._animations != None:
                for animation in sublayer.animations:
                    item.child(item.childCount()-1).addChild(QTreeWidgetItem(
                        [animation.keyPath, "Animation"]))

    def openInInspector(self, current, _):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.insertRow(0)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("name"))
        self.ui.tableWidget.item(0, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(current.text(0)))
        # print(self.cafile.find(current.text(2)))
        print(current.text(0), current.text(2))  # get name and id
