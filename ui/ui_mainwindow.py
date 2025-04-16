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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpenPoster.sizePolicy().hasHeightForWidth())
        OpenPoster.setSizePolicy(sizePolicy)
        OpenPoster.setMinimumSize(QSize(1000, 600))
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
"    color: palette(text);\n"
"    background-color: transparent;\n"
"	spacing: 0px;\n"
"}\n"
"\n"
"QWidget:focus {\n"
"    outline: none;\n"
"}\n"
"\n"
"QWidget [cls=central] {\n"
"    background-color: palette(base);\n"
"	border-radius: 0px;\n"
"	border: 1px solid palette(mid);\n"
"}\n"
"\n"
"QLabel {\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QToolButton {\n"
"    background-color: palette(button);\n"
"    border: none;\n"
"    color: palette(text);\n"
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
"    background-color: palette(dark);\n"
"    color: palette(text);\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"QCheckBox {\n"
"	spacing: 8px;\n"
"	font-size: 14px;\n"
"}"
                        "\n"
"\n"
"QRadioButton {\n"
"	spacing: 8px;\n"
"	font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	color: palette(text);\n"
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
"    background: palette(mid);\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:pressed {\n"
"    background: palette(dark);\n"
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
"    background-color: palette(mid);\n"
"    height: 4px;\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: palette(dark);\n"
"    width: 8px;\n"
"    margin: -8px 0;\n"
"    border-radius: 4px;\n"
""
                        "}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: palette(highlight);\n"
"}\n"
"\n"
"QSlider::tick:horizontal {\n"
"    background-color: palette(dark);\n"
"    width: 1px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    color: palette(text);\n"
"    padding: 5px;\n"
"    border: 1px solid palette(mid);\n"
"    height: 30px;\n"
"}\n"
"\n"
"QTableView, QTreeView {\n"
"    border: none;\n"
"    selection-background-color: palette(highlight);\n"
"    selection-color: palette(highlighted-text);\n"
"}\n"
"\n"
"QTreeView::item {\n"
"    min-height: 30px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QPushButton, QLabel[clickable=\"true\"] {\n"
"    border-radius: 6px;\n"
"    padding: 5px 10px;\n"
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
        self.filesWidget = QWidget(self.body)
        self.filesWidget.setObjectName(u"filesWidget")
        self.filesWidget.setStyleSheet(u"border: 1px solid #4B4B4B; border-radius: 4px; padding: 4px;")
        self.filesLayout = QVBoxLayout(self.filesWidget)
        self.filesLayout.setObjectName(u"filesLayout")
        self.filesLabel = QLabel(self.filesWidget)
        self.filesLabel.setObjectName(u"filesLabel")

        self.filesLayout.addWidget(self.filesLabel)

        self.treeWidget = QTreeWidget(self.filesWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setIconSize(QSize(24, 24))
        self.treeWidget.setIndentation(20)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setMinimumSectionSize(100)
        self.treeWidget.header().setDefaultSectionSize(200)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setStretchLastSection(True)

        self.filesLayout.addWidget(self.treeWidget)


        self.horizontalLayout.addWidget(self.filesWidget)

        self.verticalWidget = QWidget(self.body)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalWidget.setStyleSheet(u"border: 1px solid #4B4B4B; border-radius: 4px; padding: 4px;")
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
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(220)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(25)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout.addWidget(self.tableWidget)


        self.horizontalLayout.addWidget(self.verticalWidget)

        self.openFile = QPushButton(self.centralwidget)
        self.openFile.setObjectName(u"openFile")
        self.openFile.setGeometry(QRect(10, 10, 100, 41))
        self.openFile.setAutoFillBackground(True)
        self.openFile.setStyleSheet(u"QPushButton {\n"
"  border: 1.5px solid palette(highlight);\n"
"  border-radius: 8px;\n"
"  padding: 5px 10px;\n"
"  background-color: rgba(80, 120, 200, 30);\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: rgba(60, 100, 180, 120);\n"
"}")
        self.filename = QLabel(self.centralwidget)
        self.filename.setObjectName(u"filename")
        self.filename.setGeometry(QRect(120, 20, 600, 30))
        self.filename.setMinimumSize(QSize(200, 30))
        self.filename.setMaximumSize(QSize(800, 16777215))
        self.filename.setStyleSheet(u"border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px; color: #666666; font-style: italic;")
        self.filename.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        OpenPoster.setCentralWidget(self.centralwidget)

        self.retranslateUi(OpenPoster)

        QMetaObject.connectSlotsByName(OpenPoster)
    # setupUi

    def retranslateUi(self, OpenPoster):
        OpenPoster.setWindowTitle(QCoreApplication.translate("OpenPoster", u"OpenPoster", None))
        self.filesLabel.setText(QCoreApplication.translate("OpenPoster", u"Files", None))
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

