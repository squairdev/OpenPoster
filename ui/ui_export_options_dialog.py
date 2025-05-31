# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_options_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)
import resources_rc

class Ui_ExportOptionsDialog(object):
    def setupUi(self, ExportOptionsDialog):
        if not ExportOptionsDialog.objectName():
            ExportOptionsDialog.setObjectName(u"ExportOptionsDialog")
        ExportOptionsDialog.resize(580, 250)
        ExportOptionsDialog.setModal(True)
        self.mainLayout = QVBoxLayout(ExportOptionsDialog)
        self.mainLayout.setObjectName(u"mainLayout")
        self.titleLabel = QLabel(ExportOptionsDialog)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.titleLabel)

        self.optionsLayout = QHBoxLayout()
        self.optionsLayout.setObjectName(u"optionsLayout")
        self.optionsLayout.setContentsMargins(-1, 20, -1, -1)
        self.copyButton = QToolButton(ExportOptionsDialog)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setIconSize(QSize(64, 64))
        self.copyButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.copyButton.setFixedSize(QSize(180, 180))

        self.optionsLayout.addWidget(self.copyButton)

        self.tendiesButton = QToolButton(ExportOptionsDialog)
        self.tendiesButton.setObjectName(u"tendiesButton")
        self.tendiesButton.setIconSize(QSize(64, 64))
        self.tendiesButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tendiesButton.setFixedSize(QSize(180, 180))

        self.optionsLayout.addWidget(self.tendiesButton)

        self.nuggetButton = QToolButton(ExportOptionsDialog)
        self.nuggetButton.setObjectName(u"nuggetButton")
        icon = QIcon()
        icon.addFile(u":/assets/nugget.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nuggetButton.setIcon(icon)
        self.nuggetButton.setIconSize(QSize(64, 64))
        self.nuggetButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nuggetButton.setFixedSize(QSize(180, 180))

        self.optionsLayout.addWidget(self.nuggetButton)


        self.mainLayout.addLayout(self.optionsLayout)


        self.retranslateUi(ExportOptionsDialog)

        QMetaObject.connectSlotsByName(ExportOptionsDialog)
    # setupUi

    def retranslateUi(self, ExportOptionsDialog):
        ExportOptionsDialog.setWindowTitle(QCoreApplication.translate("ExportOptionsDialog", u"Export Options", None))
        self.titleLabel.setText(QCoreApplication.translate("ExportOptionsDialog", u"How would you like to export?", None))
        self.titleLabel.setStyleSheet(QCoreApplication.translate("ExportOptionsDialog", u"font-size:18px; font-weight:bold;", None))
        self.copyButton.setText(QCoreApplication.translate("ExportOptionsDialog", u"Export as a copy", None))
        self.tendiesButton.setText(QCoreApplication.translate("ExportOptionsDialog", u"Export as .tendies", None))
        self.nuggetButton.setText(QCoreApplication.translate("ExportOptionsDialog", u"Export to Nugget", None))
    # retranslateUi

