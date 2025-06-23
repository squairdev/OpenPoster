import sys
import os
import platform
import shutil
import tempfile
import webbrowser
import re

from PySide6 import QtCore
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QApplication, QFileDialog, QInputDialog,
                             QWidget, QHBoxLayout, QLabel, QComboBox, QTableWidgetItem,
                             QGraphicsRectItem, QGraphicsTextItem, QGraphicsPixmapItem,
                             QTreeWidgetItem, QTreeWidgetItemIterator)
from PySide6.QtGui import (QIcon, QColor, QPalette, QShortcut, QKeySequence,
                         QFont, QPixmap, QTransform)
from PySide6.QtCore import Qt, QRectF, QPointF, QStandardPaths, QVariantAnimation, QEvent, QTranslator

from .file_operations import FileOperationsMixin
from .preview_rendering import PreviewRenderingMixin
from .inspector_management import InspectorManagementMixin
from .ui_components import UIComponentsMixin

from ._formatter import Format
from ._parse import Parse
from ._applyanimation import ApplyAnimation
from ._assets import Assets
from ui.ui_mainwindow import Ui_OpenPoster
from lib.ca_elements.core.cafile import CAFile
from lib.ca_elements.core.calayer import CALayer
from .custom_widgets import CheckerboardGraphicsScene
from .settings_window import SettingsDialog
from .exportoptions_window import ExportOptionsDialog


class MainWindow(QMainWindow, FileOperationsMixin, PreviewRenderingMixin,
                 InspectorManagementMixin, UIComponentsMixin):
    def __init__(self, config_manager, translator):
        super().__init__()
        self.scene = None
        self.config_manager = config_manager
        self.translator = translator

        # State management
        self.isDirty = False
        self.animations_playing = False
        self.animations = []
        self.shortcuts_list = []
        self.theme_change_callbacks = []

        # Initialize core components
        self.initAssetFinder()
        self.bindOperationFunctions()
        self.loadIconResources()

        # Setup UI
        self.initUI()
        self.loadThemeFromConfig()
        self.loadWindowGeometry()
        self.setupShortcuts()

    def initAssetFinder(self):
        if hasattr(sys, '_MEIPASS'):
            self.app_base_path = sys._MEIPASS
        else:
            self.app_base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        self.cachedImages = {}
        self.missing_assets = set()
        self.cafilepath = ""

    def bindOperationFunctions(self):
        # TEMPORARY NAMES
        self._format = Format()
        self.formatFloat = self._format.formatFloat
        self.formatPoint = self._format.formatPoint

        self._parse = Parse()
        self.parseTransform = self._parse.parseTransform
        self.parseColor = self._parse.parseColor

        self._applyAnimation = ApplyAnimation(self.scene)
        self.applyAnimationsToPreview = self._applyAnimation.applyAnimationsToPreview
        self.applyKeyframeAnimationToItem = self._applyAnimation.applyKeyframeAnimationToItem
        self.applyTransitionAnimationToPreview = self._applyAnimation.applyTransitionAnimationToPreview
        self.applySpringAnimationToItem = self._applyAnimation.applySpringAnimationToItem

        self.findAssetPath = lambda src_path: Assets.findAssetPath(self, src_path)
        self.loadImage = lambda src_path: Assets.loadImage(self, src_path)

    def loadIconResources(self):
        self.editIcon = QIcon(":/icons/edit.svg")
        self.editIconWhite = QIcon(":/icons/edit-white.svg")
        self.playIcon = QIcon(":/icons/play.svg")
        self.playIconWhite = QIcon(":/icons/play-white.svg")
        self.pauseIcon = QIcon(":/icons/pause.svg")
        self.pauseIconWhite = QIcon(":/icons/pause-white.svg")
        self.settingsIcon = QIcon(":/icons/settings.svg")
        self.settingsIconWhite = QIcon(":/icons/settings-white.svg")
        self.discordIcon = QIcon(":/icons/discord.svg")
        self.discordIconWhite = QIcon(":/icons/discord-white.svg")
        self.exportIcon = QIcon(":/icons/export.svg")
        self.exportIconWhite = QIcon(":/icons/export-white.svg")
        self.addIcon = QIcon(":/icons/add.svg")
        self.addIconWhite = QIcon(":/icons/add-white.svg")
        self.isDarkMode = False

    def changeEvent(self, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
            self.updateCategoryHeaders()
        super().changeEvent(event)

    def retranslateUi(self):
        self.ui.retranslateUi(self)

    def load_language(self, lang_code: str):
        app = QApplication.instance()
        if app is None:
            print("Error: QApplication instance not found.")
            return

        if hasattr(app, 'translator') and app.translator is not None:
            app.removeTranslator(app.translator)

        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        qm_dir_path = os.path.join(base_path, "languages")

        new_translator = QTranslator()
        if new_translator.load(f"app_{lang_code}", qm_dir_path):
            app.installTranslator(new_translator)
            app.translator = new_translator
            print(f"Successfully loaded and installed translation for: {lang_code}")
        else:
            print(f"Failed to load translation for {lang_code} from {qm_dir_path}.")

        QApplication.postEvent(self, QEvent(QEvent.Type.LanguageChange))
