# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QKeySequenceEdit, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(600, 400)
        self.mainLayout = QHBoxLayout(SettingsDialog)
        self.mainLayout.setObjectName(u"mainLayout")
        self.tabWidget = QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.uiTab = QWidget()
        self.uiTab.setObjectName(u"uiTab")
        self.uiTabLayout = QVBoxLayout(self.uiTab)
        self.uiTabLayout.setObjectName(u"uiTabLayout")
        self.uiTabLayout.setAlignment(Qt.AlignTop)
        self.rememberRowLayout = QHBoxLayout()
        self.rememberRowLayout.setObjectName(u"rememberRowLayout")
        self.rememberLabel = QLabel(self.uiTab)
        self.rememberLabel.setObjectName(u"rememberLabel")

        self.rememberRowLayout.addWidget(self.rememberLabel)

        self.rememberSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.rememberRowLayout.addItem(self.rememberSpacer)

        self.rememberWindowCheckbox = QCheckBox(self.uiTab)
        self.rememberWindowCheckbox.setObjectName(u"rememberWindowCheckbox")

        self.rememberRowLayout.addWidget(self.rememberWindowCheckbox)


        self.uiTabLayout.addLayout(self.rememberRowLayout)

        self.resetPanelsRowLayout = QHBoxLayout()
        self.resetPanelsRowLayout.setObjectName(u"resetPanelsRowLayout")
        self.resetPanelsLabel = QLabel(self.uiTab)
        self.resetPanelsLabel.setObjectName(u"resetPanelsLabel")

        self.resetPanelsRowLayout.addWidget(self.resetPanelsLabel)

        self.resetPanelsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resetPanelsRowLayout.addItem(self.resetPanelsSpacer)

        self.resetPanelsButton = QPushButton(self.uiTab)
        self.resetPanelsButton.setObjectName(u"resetPanelsButton")

        self.resetPanelsRowLayout.addWidget(self.resetPanelsButton)


        self.uiTabLayout.addLayout(self.resetPanelsRowLayout)

        self.tabWidget.addTab(self.uiTab, "")
        self.nuggetTab = QWidget()
        self.nuggetTab.setObjectName(u"nuggetTab")
        self.nuggetTabLayout = QVBoxLayout(self.nuggetTab)
        self.nuggetTabLayout.setObjectName(u"nuggetTabLayout")
        self.nuggetTabLayout.setAlignment(Qt.AlignTop)
        self.nuggetPathRowLayout = QHBoxLayout()
        self.nuggetPathRowLayout.setObjectName(u"nuggetPathRowLayout")
        self.nuggetLabel = QLabel(self.nuggetTab)
        self.nuggetLabel.setObjectName(u"nuggetLabel")

        self.nuggetPathRowLayout.addWidget(self.nuggetLabel)

        self.nuggetPathLineEdit = QLineEdit(self.nuggetTab)
        self.nuggetPathLineEdit.setObjectName(u"nuggetPathLineEdit")

        self.nuggetPathRowLayout.addWidget(self.nuggetPathLineEdit)

        self.nuggetBrowseButton = QPushButton(self.nuggetTab)
        self.nuggetBrowseButton.setObjectName(u"nuggetBrowseButton")

        self.nuggetPathRowLayout.addWidget(self.nuggetBrowseButton)


        self.nuggetTabLayout.addLayout(self.nuggetPathRowLayout)

        self.tabWidget.addTab(self.nuggetTab, "")
        self.shortcutsTab = QWidget()
        self.shortcutsTab.setObjectName(u"shortcutsTab")
        self.shortcutsTabLayout = QVBoxLayout(self.shortcutsTab)
        self.shortcutsTabLayout.setObjectName(u"shortcutsTabLayout")
        self.shortcutsTabLayout.setAlignment(Qt.AlignTop)
        self.exportShortcutRowLayout = QHBoxLayout()
        self.exportShortcutRowLayout.setObjectName(u"exportShortcutRowLayout")
        self.exportShortcutLabel = QLabel(self.shortcutsTab)
        self.exportShortcutLabel.setObjectName(u"exportShortcutLabel")

        self.exportShortcutRowLayout.addWidget(self.exportShortcutLabel)

        self.exportKeySequenceEdit = QKeySequenceEdit(self.shortcutsTab)
        self.exportKeySequenceEdit.setObjectName(u"exportKeySequenceEdit")
        self.exportKeySequenceEdit.setFocusPolicy(Qt.ClickFocus)

        self.exportShortcutRowLayout.addWidget(self.exportKeySequenceEdit)

        self.exportShortcutResetButton = QPushButton(self.shortcutsTab)
        self.exportShortcutResetButton.setObjectName(u"exportShortcutResetButton")

        self.exportShortcutRowLayout.addWidget(self.exportShortcutResetButton)


        self.shortcutsTabLayout.addLayout(self.exportShortcutRowLayout)

        self.zoomInShortcutRowLayout = QHBoxLayout()
        self.zoomInShortcutRowLayout.setObjectName(u"zoomInShortcutRowLayout")
        self.zoomInShortcutLabel = QLabel(self.shortcutsTab)
        self.zoomInShortcutLabel.setObjectName(u"zoomInShortcutLabel")

        self.zoomInShortcutRowLayout.addWidget(self.zoomInShortcutLabel)

        self.zoomInKeySequenceEdit = QKeySequenceEdit(self.shortcutsTab)
        self.zoomInKeySequenceEdit.setObjectName(u"zoomInKeySequenceEdit")
        self.zoomInKeySequenceEdit.setFocusPolicy(Qt.ClickFocus)

        self.zoomInShortcutRowLayout.addWidget(self.zoomInKeySequenceEdit)

        self.zoomInShortcutResetButton = QPushButton(self.shortcutsTab)
        self.zoomInShortcutResetButton.setObjectName(u"zoomInShortcutResetButton")

        self.zoomInShortcutRowLayout.addWidget(self.zoomInShortcutResetButton)


        self.shortcutsTabLayout.addLayout(self.zoomInShortcutRowLayout)

        self.zoomOutShortcutRowLayout = QHBoxLayout()
        self.zoomOutShortcutRowLayout.setObjectName(u"zoomOutShortcutRowLayout")
        self.zoomOutShortcutLabel = QLabel(self.shortcutsTab)
        self.zoomOutShortcutLabel.setObjectName(u"zoomOutShortcutLabel")

        self.zoomOutShortcutRowLayout.addWidget(self.zoomOutShortcutLabel)

        self.zoomOutKeySequenceEdit = QKeySequenceEdit(self.shortcutsTab)
        self.zoomOutKeySequenceEdit.setObjectName(u"zoomOutKeySequenceEdit")
        self.zoomOutKeySequenceEdit.setFocusPolicy(Qt.ClickFocus)

        self.zoomOutShortcutRowLayout.addWidget(self.zoomOutKeySequenceEdit)

        self.zoomOutShortcutResetButton = QPushButton(self.shortcutsTab)
        self.zoomOutShortcutResetButton.setObjectName(u"zoomOutShortcutResetButton")

        self.zoomOutShortcutRowLayout.addWidget(self.zoomOutShortcutResetButton)


        self.shortcutsTabLayout.addLayout(self.zoomOutShortcutRowLayout)

        self.closeWindowShortcutRowLayout = QHBoxLayout()
        self.closeWindowShortcutRowLayout.setObjectName(u"closeWindowShortcutRowLayout")
        self.closeWindowShortcutLabel = QLabel(self.shortcutsTab)
        self.closeWindowShortcutLabel.setObjectName(u"closeWindowShortcutLabel")

        self.closeWindowShortcutRowLayout.addWidget(self.closeWindowShortcutLabel)

        self.closeWindowKeySequenceEdit = QKeySequenceEdit(self.shortcutsTab)
        self.closeWindowKeySequenceEdit.setObjectName(u"closeWindowKeySequenceEdit")
        self.closeWindowKeySequenceEdit.setFocusPolicy(Qt.ClickFocus)

        self.closeWindowShortcutRowLayout.addWidget(self.closeWindowKeySequenceEdit)

        self.closeWindowShortcutResetButton = QPushButton(self.shortcutsTab)
        self.closeWindowShortcutResetButton.setObjectName(u"closeWindowShortcutResetButton")

        self.closeWindowShortcutRowLayout.addWidget(self.closeWindowShortcutResetButton)


        self.shortcutsTabLayout.addLayout(self.closeWindowShortcutRowLayout)

        self.resetAllShortcutsButton = QPushButton(self.shortcutsTab)
        self.resetAllShortcutsButton.setObjectName(u"resetAllShortcutsButton")

        self.shortcutsTabLayout.addWidget(self.resetAllShortcutsButton)

        self.tabWidget.addTab(self.shortcutsTab, "")
        self.languagesTab = QWidget()
        self.languagesTab.setObjectName(u"languagesTab")
        self.languagesTabLayout = QVBoxLayout(self.languagesTab)
        self.languagesTabLayout.setObjectName(u"languagesTabLayout")
        self.languageListWidget = QListWidget(self.languagesTab)
        self.languageListWidget.setObjectName(u"languageListWidget")

        self.languagesTabLayout.addWidget(self.languageListWidget)

        self.languageAiTranslationLabel = QLabel(self.languagesTab)
        self.languageAiTranslationLabel.setObjectName(u"languageAiTranslationLabel")
        self.languageAiTranslationLabel.setAlignment(Qt.AlignCenter)
        self.languageAiTranslationLabel.setWordWrap(True)

        self.languagesTabLayout.addWidget(self.languageAiTranslationLabel)

        self.tabWidget.addTab(self.languagesTab, "")
        self.aboutTab = QWidget()
        self.aboutTab.setObjectName(u"aboutTab")
        self.aboutTabLayout = QVBoxLayout(self.aboutTab)
        self.aboutTabLayout.setObjectName(u"aboutTabLayout")
        self.aboutTabLayout.setContentsMargins(20, 40, 20, 20)
        self.titleLabel = QLabel(self.aboutTab)
        self.titleLabel.setObjectName(u"titleLabel")

        self.aboutTabLayout.addWidget(self.titleLabel)

        self.versionLabel = QLabel(self.aboutTab)
        self.versionLabel.setObjectName(u"versionLabel")

        self.aboutTabLayout.addWidget(self.versionLabel)

        self.guiLabel = QLabel(self.aboutTab)
        self.guiLabel.setObjectName(u"guiLabel")

        self.aboutTabLayout.addWidget(self.guiLabel)

        self.creditsLabel = QLabel(self.aboutTab)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setText(u"<b>Contributors:</b>\n"
"        <ul>\n"
"        <li>retronbv - Owner, Manages libraries</li>\n"
"        <li>enkei64 - GUI, Features developer</li>\n"
"        <li>ItMe12s - QoL additions, features suggestions</li>\n"
"        <li>AnhNguyenlost13 - Building/Compiling</li>\n"
"        <li>LeminLimez - Signing and Nugget support</li>\n"
"        <li>SuperEVILFACE - CAAnimation Class</li>\n"
"        </ul>")
        self.creditsLabel.setTextFormat(Qt.RichText)
        self.creditsLabel.setWordWrap(True)

        self.aboutTabLayout.addWidget(self.creditsLabel)

        self.websiteLabel = QLabel(self.aboutTab)
        self.websiteLabel.setObjectName(u"websiteLabel")
        self.websiteLabel.setOpenExternalLinks(True)

        self.aboutTabLayout.addWidget(self.websiteLabel)

        self.licenseLabel = QLabel(self.aboutTab)
        self.licenseLabel.setObjectName(u"licenseLabel")
        self.licenseLabel.setOpenExternalLinks(True)

        self.aboutTabLayout.addWidget(self.licenseLabel)

        self.discordButton = QPushButton(self.aboutTab)
        self.discordButton.setObjectName(u"discordButton")
        self.discordButton.setIconSize(QSize(24, 24))

        self.aboutTabLayout.addWidget(self.discordButton)

        self.tabWidget.addTab(self.aboutTab, "")

        self.mainLayout.addWidget(self.tabWidget)


        self.retranslateUi(SettingsDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.rememberLabel.setText(QCoreApplication.translate("SettingsDialog", u"Remember window size and position", None))
        self.resetPanelsLabel.setText(QCoreApplication.translate("SettingsDialog", u"Reset panels to default sizes", None))
        self.resetPanelsButton.setText(QCoreApplication.translate("SettingsDialog", u"Click here to reset all panels", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.uiTab), QCoreApplication.translate("SettingsDialog", u"UI", None))
        self.nuggetLabel.setText(QCoreApplication.translate("SettingsDialog", u"Nugget Executable:", None))
        self.nuggetBrowseButton.setText(QCoreApplication.translate("SettingsDialog", u"Browse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nuggetTab), QCoreApplication.translate("SettingsDialog", u"Nugget", None))
        self.exportShortcutLabel.setText(QCoreApplication.translate("SettingsDialog", u"Export Shortcut:", None))
        self.exportShortcutResetButton.setText(QCoreApplication.translate("SettingsDialog", u"Reset", None))
        self.zoomInShortcutLabel.setText(QCoreApplication.translate("SettingsDialog", u"Zoom In Shortcut:", None))
        self.zoomInShortcutResetButton.setText(QCoreApplication.translate("SettingsDialog", u"Reset", None))
        self.zoomOutShortcutLabel.setText(QCoreApplication.translate("SettingsDialog", u"Zoom Out Shortcut:", None))
        self.zoomOutShortcutResetButton.setText(QCoreApplication.translate("SettingsDialog", u"Reset", None))
        self.closeWindowShortcutLabel.setText(QCoreApplication.translate("SettingsDialog", u"Close Window Shortcut:", None))
        self.closeWindowShortcutResetButton.setText(QCoreApplication.translate("SettingsDialog", u"Reset", None))
        self.resetAllShortcutsButton.setText(QCoreApplication.translate("SettingsDialog", u"Reset All Shortcuts", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shortcutsTab), QCoreApplication.translate("SettingsDialog", u"Shortcuts", None))
        self.languageAiTranslationLabel.setText(QCoreApplication.translate("SettingsDialog", u"Chinese, French, Italian, Japanese, Korean, and Thai translations by AI (Gemini 2.5 Pro).", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.languagesTab), QCoreApplication.translate("SettingsDialog", u"Languages", None))
        self.titleLabel.setText(QCoreApplication.translate("SettingsDialog", u"<h2>OpenPoster Beta</h2>", None))
        self.versionLabel.setText(QCoreApplication.translate("SettingsDialog", u"Version: v{__version__}", None))
        self.guiLabel.setText(QCoreApplication.translate("SettingsDialog", u"GUI: PySide6", None))
        self.websiteLabel.setText(QCoreApplication.translate("SettingsDialog", u"<a href=\"https://openposter.pages.dev\">openposter.pages.dev</a>", None))
        self.licenseLabel.setText(QCoreApplication.translate("SettingsDialog", u"<a href=\"https://github.com/openposter/OpenPoster/blob/main/LICENSE\">MIT License</a>", None))
        self.discordButton.setText(QCoreApplication.translate("SettingsDialog", u"  Join Discord", None))
        self.discordButton.setStyleSheet(QCoreApplication.translate("SettingsDialog", u"padding-left: 8px;", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aboutTab), QCoreApplication.translate("SettingsDialog", u"About", None))
    # retranslateUi

