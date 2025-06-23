from PySide6.QtGui import QIcon, QPalette, QColor, QFont, QKeySequence, QShortcut, QAction, QPixmap
from PySide6.QtWidgets import QMenu, QGraphicsDropShadowEffect, QInputDialog, QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import Qt, QEvent
from .settings_window import SettingsDialog
from .custom_widgets import CheckerboardGraphicsScene
from lib.ca_elements.core import CALayer
import os
import sys
import platform
from ui.ui_mainwindow import Ui_OpenPoster

class UIComponentsMixin:
    def loadThemeFromConfig(self):
        theme = self.config_manager.get_config("ui_theme", "dark")
        self.isDarkMode = theme == "dark"
        if self.isDarkMode:
            self.applyDarkModeStyles()
        else:
            self.applyLightModeStyles()
        self.updateButtonIcons()
        self.updateCategoryHeaders()

    def updateButtonIcons(self):
        if not hasattr(self, 'ui'):
            return

        if hasattr(self.ui, 'editButton'):
            self.ui.editButton.setIcon(self.editIconWhite if self.isDarkMode else self.editIcon)
        
        if hasattr(self.ui, 'playButton'):
            if self.animations_playing:
                self.ui.playButton.setIcon(self.pauseIconWhite if self.isDarkMode else self.pauseIcon)
                self.ui.playButton.setToolTip("Playing (Click to Pause)")
            else:
                self.ui.playButton.setIcon(self.playIconWhite if self.isDarkMode else self.playIcon)
                self.ui.playButton.setToolTip("Paused/Stopped (Click to Play)")

        if hasattr(self.ui, 'settingsButton'):
            self.ui.settingsButton.setIcon(self.settingsIconWhite if self.isDarkMode else self.settingsIcon)
        
        if hasattr(self.ui, 'exportButton'):
            self.ui.exportButton.setIcon(self.exportIconWhite if self.isDarkMode else self.exportIcon)

        if hasattr(self.ui, 'addButton'):
            self.ui.addButton.setIcon(self.addIconWhite if self.isDarkMode else self.addIcon)

    def updateCategoryHeaders(self):
        if not hasattr(self, 'ui') or not hasattr(self.ui, 'tableWidget'):
            return
            
        if self.isDarkMode:
            bg_color = QColor(60, 60, 60)
            text_color = QColor(230, 230, 230)
        else:
            bg_color = QColor(220, 220, 220)
            text_color = QColor(30, 30, 30)
            
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 0)
            if item and self.ui.tableWidget.columnSpan(row, 0) > 1:
                item.setBackground(bg_color)
                item.setForeground(text_color)

    def setupSystemAppearanceDetection(self):
        try:
            from Foundation import NSUserDefaults
            self.macAppearanceObserver = NSUserDefaults.standardUserDefaults()
            self.updateAppearanceForMac()
            
            self.app = QApplication.instance()
            self.app.installEventFilter(self)
        except ImportError:
            print("Foundation module not available - dark mode detection limited")
            self.detectDarkMode()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ApplicationPaletteChange:
            self.updateAppearanceForMac()
        return super(UIComponentsMixin, self).eventFilter(obj, event)

    def updateAppearanceForMac(self):
        previous_dark_mode = self.isDarkMode
        current_system_is_dark = False
        try:
            from Foundation import NSUserDefaults
            appleInterfaceStyle = NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle")
            current_system_is_dark = appleInterfaceStyle == "Dark"
        except Exception as e:
            pass

        if self.config_manager.get_config("ui_theme", "system") == "system":
            if current_system_is_dark != previous_dark_mode:
                self.isDarkMode = current_system_is_dark
                self.loadThemeFromConfig()

    def applyDarkModeStyles(self):
        if not hasattr(self, 'ui'): return
        qss_path = self.findAssetPath("themes/dark_style.qss")
        if qss_path:
            try:
                with open(qss_path, "r") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error applying dark_style.qss: {e}")
        
        scene = getattr(self, 'scene', None)
        if scene:
            scene.setBackgroundColor(QColor(50, 50, 50), QColor(40, 40, 40))
            scene.update()
        
        self.updateButtonIcons() 
        self.updateCategoryHeaders()

    def applyLightModeStyles(self):
        if not hasattr(self, 'ui'): return
        qss_path = self.findAssetPath("themes/light_style.qss")
        if qss_path:
            try:
                with open(qss_path, "r") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error applying light_style.qss: {e}")

        scene = getattr(self, 'scene', None)
        if scene:
            scene.setBackgroundColor(QColor(240, 240, 240), QColor(220, 220, 220))
            scene.update()
        
        self.updateButtonIcons() 
        self.updateCategoryHeaders()

    def initUI(self):
        self.ui = Ui_OpenPoster()
        self.ui.setupUi(self)
        self.isMacOS = platform.system() == "Darwin"

        # Connect core signals
        self.ui.treeWidget.currentItemChanged.connect(self.openInInspector)
        self.ui.statesTreeWidget.currentItemChanged.connect(self.openStateInInspector)
        self.ui.tableWidget.itemChanged.connect(self.onInspectorChanged)
        
        if hasattr(self.ui, 'editButton'):
            self.ui.editButton.hide()
            self.ui.editButton.setEnabled(False)
        
        self.ui.playButton.setIcon(self.playIconWhite if self.isDarkMode else self.playIcon) 
        self.ui.playButton.clicked.connect(self.toggleAnimations)
        
        self.ui.settingsButton.setIcon(self.settingsIconWhite if self.isDarkMode else self.settingsIcon)
        self.ui.settingsButton.clicked.connect(self.showSettingsDialog)
        
        self.ui.exportButton.setIcon(self.exportIconWhite if self.isDarkMode else self.exportIcon)
        self.ui.exportButton.clicked.connect(self.exportFile)

        self.ui.addButton.setIcon(self.addIconWhite if self.isDarkMode else self.addIcon)

        self.add_menu_ui = QMenu(self)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.add_menu_ui.setGraphicsEffect(shadow)

        self.addMenuBasicAction = QAction(self)
        self.addMenuBasicAction.setText("Basic Layer")
        self.addMenuTextAction = QAction(self)
        self.addMenuTextAction.setText("Text Layer")
        self.addMenuImageAction = QAction(self)
        self.addMenuImageAction.setText("Image Layer")

        self.add_menu_ui.addAction(self.addMenuBasicAction)
        self.addMenuBasicAction.triggered.connect(lambda: self.addlayer())
        self.add_menu_ui.addAction(self.addMenuTextAction)
        self.addMenuTextAction.triggered.connect(lambda: self.addlayer(name="New Text Layer",type="text"))
        self.add_menu_ui.addAction(self.addMenuImageAction)
        self.addMenuImageAction.triggered.connect(lambda: self.addlayer(name="New Image Layer",type="image"))

        self.ui.addButton.setMenu(self.add_menu_ui)
        self.ui.addButton.setEnabled(True)

        self.ui.openFile.clicked.connect(self.openFile)
        self.ui.filename.mousePressEvent = self.toggleFilenameDisplay
        self.showFullPath = True
        
        self.scene = CheckerboardGraphicsScene()
        orig_make_item = self.scene.makeItemEditable
        def makeItemEditable(item):
            editable = orig_make_item(item)
            if editable:
                editable.itemChanged.connect(lambda it, item=item: self.onItemMoved(item))
                editable.itemIsChanging.connect(lambda it, item=item: self.onItemChanging(item))
                editable.transformChanged.connect(lambda tr, item=item: self.onTransformChanged(item, tr))
            return editable
        self.scene.makeItemEditable = makeItemEditable
        self.ui.graphicsView.setScene(self.scene)
        
        self.ui.graphicsView.setEditMode(True)

        self.scene.itemSelectedOnCanvas.connect(self.selectLayerInTree)
        
        self.ui.graphicsView.minZoom = 0.05
        self.ui.graphicsView.maxZoom = 10.0
        self.ui.graphicsView.contentFittingZoom = 0.05
        
        self.ui.mainSplitter.splitterMoved.connect(self.saveSplitterSizes)
        self.ui.layersSplitter.splitterMoved.connect(self.saveSplitterSizes)
        
        self.loadSplitterSizes()
        
        self.currentSelectedItem = None
        self.cachedImages = {}
        self.currentZoom = 1.0

    def markDirty(self):
        self.isDirty = True

    def addlayer(self, **kwargs):
        if not hasattr(self, 'cafile') or not self.cafile:
            QMessageBox.warning(self, "No File Open", "Please open or create a file before adding a layer.")
            return

        # --- Calculate new layer size ---
        root_bounds = self.cafile.rootlayer.bounds
        root_w = float(root_bounds[2])
        root_h = float(root_bounds[3])
        
        new_h = root_h * 0.2
        new_w = new_h
        
        layer_type = kwargs.get("type")
        if layer_type == "text":
            new_w = root_w * 0.2

        layer = CALayer(**kwargs)
        
        if layer_type != "image":
             layer.bounds = ["0", "0", str(new_w), str(new_h)]

        if layer_type == "text":
            input_dialog = QInputDialog(self)
            input_dialog.setWindowTitle("New Text Layer")
            input_dialog.setLabelText("Enter text:")
            input_dialog.setTextValue(getattr(layer, "string", ""))
            
            if hasattr(self, 'isDarkMode') and self.isDarkMode:
                input_dialog.setStyleSheet(
                    "QInputDialog { background-color: #303030; color: #D0D0D0; }"
                    "QInputDialog QLabel { color: #D0D0D0; }"
                    "QInputDialog QLineEdit { background-color: #3A3A3A; color: #D0D0D0; border: 1px solid #606060; border-radius: 4px; padding: 4px; }"
                    "QInputDialog QPushButton { border: 1px solid #606060; border-radius: 6px; padding: 5px 10px; background-color: #3A3A3A; color: #D0D0D0; }"
                )
            
            if input_dialog.exec():
                text = input_dialog.textValue()
                if not text:
                    return
                layer.string = text
            else:
                return
        elif layer_type == "image":
            image_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if not image_path:
                return
            layer.content.src = image_path

        if hasattr(self, "currentInspectObject"):
            element = self.currentInspectObject
        else:
            element = self.cafile.rootlayer

        element.addlayer(layer)
        self.ui.treeWidget.clear()
        self.populateLayersTreeWidget()
        self.renderPreview(self.cafile.rootlayer)

    def setupShortcuts(self):
        for shortcut_item in self.shortcuts_list:
            shortcut_item.setEnabled(False)
            shortcut_item.activated.disconnect()
        self.shortcuts_list.clear()

        settings_shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Preferences), self)
        settings_shortcut.activated.connect(self.showSettingsDialog)
        self.shortcuts_list.append(settings_shortcut)

        open_file_shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Open), self)
        open_file_shortcut.activated.connect(self.openFile)
        self.shortcuts_list.append(open_file_shortcut)

        export_shortcut_str = self.config_manager.get_export_shortcut()
        if export_shortcut_str:
            export_shortcut = QShortcut(QKeySequence(export_shortcut_str), self)
            export_shortcut.activated.connect(self.exportFile)
            self.shortcuts_list.append(export_shortcut)

        zoom_in_shortcut_str = self.config_manager.get_zoom_in_shortcut()
        if zoom_in_shortcut_str:
            zoom_in_shortcut = QShortcut(QKeySequence(zoom_in_shortcut_str), self)
            zoom_in_shortcut.activated.connect(self.zoomIn)
            self.shortcuts_list.append(zoom_in_shortcut)

        zoom_out_shortcut_str = self.config_manager.get_zoom_out_shortcut()
        if zoom_out_shortcut_str:
            zoom_out_shortcut = QShortcut(QKeySequence(zoom_out_shortcut_str), self)
            zoom_out_shortcut.activated.connect(self.zoomOut)
            self.shortcuts_list.append(zoom_out_shortcut)

        close_window_shortcut_str = self.config_manager.get_close_window_shortcut()
        if close_window_shortcut_str:
            close_window_shortcut = QShortcut(QKeySequence(close_window_shortcut_str), self)
            close_window_shortcut.activated.connect(self.close)
            self.shortcuts_list.append(close_window_shortcut)

        play_pause_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        play_pause_shortcut.activated.connect(self.toggleAnimations)
        self.shortcuts_list.append(play_pause_shortcut)

    def showSettingsDialog(self):
        if hasattr(self, 'config_manager'):
            settings_dialog = SettingsDialog(self, self.config_manager)
            settings_dialog.exec()
            self.setupShortcuts()

    def saveSplitterSizes(self):
        if hasattr(self, 'ui') and hasattr(self.ui, 'mainSplitter'):
            sizes = self.ui.mainSplitter.sizes()
            self.config_manager.save_splitter_sizes("mainSplitter", sizes)
            
        if hasattr(self, 'ui') and hasattr(self.ui, 'layersSplitter'):
            sizes = self.ui.layersSplitter.sizes()
            self.config_manager.save_splitter_sizes("layersSplitter", sizes)
    
    def loadSplitterSizes(self):
        if hasattr(self, 'ui') and hasattr(self.ui, 'mainSplitter'):
            sizes = self.config_manager.get_splitter_sizes("mainSplitter")
            if sizes:
                self.ui.mainSplitter.setSizes(sizes)
                
        if hasattr(self, 'ui') and hasattr(self.ui, 'layersSplitter'):
            sizes = self.config_manager.get_splitter_sizes("layersSplitter")
            if sizes:
                self.ui.layersSplitter.setSizes(sizes)

    def loadWindowGeometry(self):
        geometry = self.config_manager.get_window_geometry()
        
        if geometry["remember_size"]:
            self.resize(geometry["size"][0], geometry["size"][1])
            self.move(geometry["position"][0], geometry["position"][1])
            
            if geometry["maximized"]:
                self.showMaximized()
                
    def saveWindowGeometry(self):
        if self.isMaximized():
            size = [self.normalGeometry().width(), self.normalGeometry().height()]
            position = [self.normalGeometry().x(), self.normalGeometry().y()]
            self.config_manager.save_window_geometry(size, position, True)
        else:
            size = [self.width(), self.height()]
            position = [self.x(), self.y()]
            self.config_manager.save_window_geometry(size, position, False)

    def closeEvent(self, event):
        if getattr(self, 'isDirty', False):
            msg = QMessageBox(self)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Are you sure you want to discard them and exit?")
            pix = QPixmap(":/assets/openposter.png")
            msg.setIconPixmap(pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            reply = msg.exec()
            if reply != QMessageBox.Yes:
                event.ignore()
                return
        
        if hasattr(self, 'tendies_temp_dir') and self.tendies_temp_dir and os.path.exists(self.tendies_temp_dir):
            try:
                shutil.rmtree(self.tendies_temp_dir)
            except Exception as e:
                print(f"Error cleaning up temporary directory: {e}")
                
        self.saveSplitterSizes()
        self.saveWindowGeometry()
        super(UIComponentsMixin, self).closeEvent(event)

    def toggleFilenameDisplay(self, event):
        if hasattr(self, 'cafilepath'):
            if self.showFullPath:
                self.ui.filename.setText(os.path.basename(self.cafilepath))
            else:
                self.ui.filename.setText(self.cafilepath)
            self.showFullPath = not self.showFullPath

    def updateFilenameDisplay(self):
        if hasattr(self, 'ui') and hasattr(self.ui, 'filename'):
            display_path = self.cafilepath if self.showFullPath else os.path.basename(self.cafilepath)
            self.ui.filename.setText(display_path)
            self.ui.filename.setToolTip(self.cafilepath)