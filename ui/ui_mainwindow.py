# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_OpenPoster(object):
    def setupUi(self, OpenPoster):
        if not OpenPoster.objectName():
            OpenPoster.setObjectName(u"OpenPoster")
        OpenPoster.resize(1000, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpenPoster.sizePolicy().hasHeightForWidth())
        OpenPoster.setSizePolicy(sizePolicy)
        OpenPoster.setMinimumSize(QSize(1000, 600))
        OpenPoster.setMaximumSize(QSize(1000, 600))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 128))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        OpenPoster.setPalette(palette)
        OpenPoster.setStyleSheet(u"QWidget {\n"
"    color: #FFFFFF;\n"
"    background-color: transparent;\n"
"	spacing: 0px;\n"
"}\n"
"\n"
"QWidget:focus {\n"
"    outline: none;\n"
"}\n"
"\n"
"QWidget [cls=central] {\n"
"    background-color: #1e1e1e;\n"
"	border-radius: 0px;\n"
"	border: 1px solid #4B4B4B;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QToolButton {\n"
"    background-color: #3b3b3b;\n"
"    border: none;\n"
"    color: #e8e8e8;\n"
"    font-size: 14px;\n"
"	min-height: 35px;\n"
"	icon-size: 16px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"QToolButton[cls=sidebarBtn] {\n"
"    background-color: transparent;\n"
"	icon-size: 24px;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: #535353;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: #2860ca;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QCheckBox {\n"
"	spacing: 8px;\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"QRadioButton {\n"
"	spacing: 8px;\n"
"	font-size: 14px;\n"
"}\n"
""
                        "\n"
"QLineEdit {\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	color: #FFFFFF;\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 8px;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 8px;\n"
"}\n"
"\n"
"QScrollBar::handle {\n"
"    background: #3b3b3b;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:pressed {\n"
"    background: #535353;\n"
"}\n"
"\n"
"QScrollBar::add-line,\n"
"QScrollBar::sub-line {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page,\n"
"QScrollBar::sub-page {\n"
"    background: none;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    background-color: #3b3b3b;\n"
"    height: 4px;\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: #535353;\n"
"    width: 8px;\n"
"    margin: -8px 0;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: #3b82f7;\n"
"}\n"
"\n"
"QSl"
                        "ider::tick:horizontal {\n"
"    background-color: #535353;\n"
"    width: 1px;\n"
"}\n"
"")
        self.centralwidget = QWidget(OpenPoster)
        self.centralwidget.setObjectName(u"centralwidget")
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        self.centralwidget.setPalette(palette1)
        self.body = QWidget(self.centralwidget)
        self.body.setObjectName(u"body")
        self.body.setGeometry(QRect(12, 60, 976, 528))
        self.body.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.body)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeWidget = QTreeWidget(self.body)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setColumnCount(2)
        self.treeWidget.header().setVisible(True)

        self.horizontalLayout.addWidget(self.treeWidget)

        self.verticalWidget = QWidget(self.body)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.verticalWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tableWidget = QTableWidget(self.verticalWidget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setColumnCount(2)

        self.verticalLayout.addWidget(self.tableWidget)


        self.horizontalLayout.addWidget(self.verticalWidget)

        self.openFile = QPushButton(self.centralwidget)
        self.openFile.setObjectName(u"openFile")
        self.openFile.setGeometry(QRect(10, 1, 100, 41))
        self.openFile.setAutoFillBackground(True)
        self.filename = QLabel(self.centralwidget)
        self.filename.setObjectName(u"filename")
        self.filename.setGeometry(QRect(120, 10, 271, 16))
        OpenPoster.setCentralWidget(self.centralwidget)

        self.retranslateUi(OpenPoster)

        QMetaObject.connectSlotsByName(OpenPoster)
    # setupUi

    def retranslateUi(self, OpenPoster):
        OpenPoster.setWindowTitle(QCoreApplication.translate("OpenPoster", u"OpenPoster", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("OpenPoster", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("OpenPoster", u"Name", None));
        self.label.setText(QCoreApplication.translate("OpenPoster", u"Inspector", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OpenPoster", u"Key", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OpenPoster", u"Value", None));
        self.openFile.setText(QCoreApplication.translate("OpenPoster", u"Open File", None))
        self.filename.setText(QCoreApplication.translate("OpenPoster", u"No File Open", None))
    # retranslateUi

