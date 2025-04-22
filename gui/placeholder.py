import sys
import os
import math
from lib.main.main import CAFile
from PySide6 import QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSize, QEvent, QVariantAnimation
from PySide6.QtGui import QPixmap, QImage, QBrush, QPen, QColor, QTransform, QPainter, QLinearGradient, QIcon
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMainWindow, QTableWidgetItem, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsTextItem, QApplication, QGraphicsView, QGraphicsItemAnimation, QPushButton, QHBoxLayout
from ui.ui_mainwindow import Ui_OpenPoster
import PySide6.QtCore as QtCore


class CheckerboardGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CheckerboardGraphicsScene, self).__init__(parent)
        self.checkerboardSize = 20

    def drawBackground(self, painter, rect):
        super(CheckerboardGraphicsScene, self).drawBackground(painter, rect)
        
        painter.save()
        painter.fillRect(rect, QColor(240, 240, 240))
        
        left = int(rect.left()) - (int(rect.left()) % self.checkerboardSize)
        top = int(rect.top()) - (int(rect.top()) % self.checkerboardSize)
        
        for x in range(left, int(rect.right()), self.checkerboardSize):
            for y in range(top, int(rect.bottom()), self.checkerboardSize):
                if (x // self.checkerboardSize + y // self.checkerboardSize) % 2 == 0:
                    painter.fillRect(x, y, self.checkerboardSize, self.checkerboardSize, QColor(220, 220, 220))
        
        painter.restore()


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None, min_zoom=0.05, max_zoom=10.0):
        super(CustomGraphicsView, self).__init__(parent)
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._last_mouse_pos = QPointF()
        self.setMouseTracking(True)
        self._panning = False
        self.minZoom = min_zoom
        self.maxZoom = max_zoom
        self.contentFittingZoom = min_zoom
    
    def wheelEvent(self, event):
        if not self.scene() or not self.scene().items():
            event.accept()
            return
            
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            angle = event.angleDelta().y()
            
            current_scale = self.transform().m11()
            zoom_factor = 1.1 if angle > 0 else 0.9
            new_scale = current_scale * zoom_factor
            new_scale = max(self.minZoom, min(self.maxZoom, new_scale))
            
            if current_scale != 0:
                scale_factor = new_scale / current_scale
            elif new_scale != 0:
                scale_factor = float('inf')

            if abs(scale_factor - 1.0) > 1e-9:
                self.scale(scale_factor, scale_factor)

        else:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - event.angleDelta().x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - event.angleDelta().y())
            
        event.accept()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._panning = True
            self._last_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super(CustomGraphicsView, self).mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._panning:
            delta = event.position() - self._last_mouse_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._last_mouse_pos = event.position()
            event.accept()
        else:
            super(CustomGraphicsView, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._panning:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super(CustomGraphicsView, self).mouseReleaseEvent(event)

    def updateContentFittingZoom(self, sceneRect):
        if sceneRect.isEmpty():
            return

        padded_rect = sceneRect.adjusted(-30, -30, 30, 30)
        
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        
        if view_width <= 0 or view_height <= 0:
            return
            
        scale_x = view_width / padded_rect.width()
        scale_y = view_height / padded_rect.height()
        
        fitting_scale = min(scale_x, scale_y)
        
        self.contentFittingZoom = max(0.01, fitting_scale * 0.9)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_OpenPoster()
        self.ui.setupUi(self)
        
        self.custom_view = CustomGraphicsView(
            parent=self.ui.previewWidget, 
            min_zoom=0.05, 
            max_zoom=10.0
        )
        self.custom_view.setObjectName("graphicsView")
        
        self.ui.previewLayout.replaceWidget(self.ui.graphicsView, self.custom_view)
        
        self.ui.graphicsView = self.custom_view
        
        self.previewHeaderLayout = QHBoxLayout()
        self.previewHeaderLayout.setObjectName("previewHeaderLayout")
        self.previewHeaderLayout.setContentsMargins(0, 0, 0, 0)
        
        self.previewHeaderLayout.addWidget(self.ui.previewLabel)
        
        self.playIcon = QIcon("icons/play.svg")
        self.pauseIcon = QIcon("icons/pause.svg")
        
        self.playButton = QPushButton(self.ui.previewWidget)
        self.playButton.setObjectName("playButton")
        self.playButton.setIcon(self.playIcon)
        self.playButton.setToolTip("Play/Pause Animations")
        self.playButton.setFixedSize(40, 40)
        self.playButton.setIconSize(QSize(32, 32))
        self.playButton.setStyleSheet("""
            QPushButton { 
                border: none; 
                background-color: transparent;
            }
            QPushButton:hover { 
                background-color: rgba(128, 128, 128, 30);
                border-radius: 20px;
            }
        """)
        self.playButton.clicked.connect(self.toggleAnimations)
        self.previewHeaderLayout.addWidget(self.playButton)
        
        self.previewHeaderLayout.addStretch()
        
        self.ui.previewLayout.removeWidget(self.ui.previewLabel)
        self.ui.previewLayout.insertLayout(0, self.previewHeaderLayout)
        
        self.animations_playing = False
        self.animations = []
        
        self.ui.openFile.clicked.connect(self.openFile)
        self.ui.treeWidget.currentItemChanged.connect(self.openInInspector)
        self.ui.statesTreeWidget.currentItemChanged.connect(self.openStateInInspector)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Key", "Value"])
        self.ui.filename.mousePressEvent = self.toggleFilenameDisplay
        self.showFullPath = True
        
        self.ui.tableWidget.verticalHeader().setVisible(False) 
        self.ui.tableWidget.setStyleSheet("QTableWidget::item { padding: 4px; }")
        header_font = self.ui.tableWidget.horizontalHeader().font()
        header_font.setPointSize(header_font.pointSize() + 2)
        self.ui.tableWidget.horizontalHeader().setFont(header_font)
        
        self.scene = CheckerboardGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.graphicsView.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.ui.graphicsView.setTransformationAnchor(self.ui.graphicsView.ViewportAnchor.AnchorUnderMouse)
        self.ui.graphicsView.setResizeAnchor(self.ui.graphicsView.ViewportAnchor.AnchorUnderMouse)
        self.ui.graphicsView.setViewportUpdateMode(self.ui.graphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        self.currentSelectedItem = None
        self.cachedImages = {}
        self.currentZoom = 1.0

    def toggleFilenameDisplay(self, event):
        if hasattr(self, 'cafilepath'):
            if self.showFullPath:
                self.ui.filename.setText(os.path.basename(self.cafilepath))
            else:
                self.ui.filename.setText(self.cafilepath)
            self.showFullPath = not self.showFullPath

    def openFile(self):
        self.ui.treeWidget.clear()
        self.ui.statesTreeWidget.clear()
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
            self.cachedImages = {}
            self.missing_assets = set()
            
            rootItem = QTreeWidgetItem([self.cafile.rootlayer.name, "Root", self.cafile.rootlayer.id, ""])
            self.ui.treeWidget.addTopLevelItem(rootItem)

            if len(self.cafile.rootlayer._sublayerorder) > 0:
                self.treeWidgetChildren(rootItem, self.cafile.rootlayer)
            
            self.populateStatesTreeWidget()
            
            self.scene.clear()
            self.currentZoom = 1.0
            self.ui.graphicsView.resetTransform()
            self.renderPreview(self.cafile.rootlayer)
            self.fitPreviewToView()
        else:
            self.ui.filename.setText("No File Open")
            self.ui.filename.setStyleSheet("border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px; color: #666666; font-style: italic;")

    def fitPreviewToView(self):
        if not hasattr(self, 'cafilepath') or not self.cafilepath:
            return
            
        all_items_rect = self.scene.itemsBoundingRect()
        
        if all_items_rect.isEmpty():
            return
            
        all_items_rect.adjust(-30, -30, 30, 30)
        
        self.ui.graphicsView.updateContentFittingZoom(all_items_rect)
        
        self.ui.graphicsView.fitInView(all_items_rect, Qt.KeepAspectRatio)
        
        transform = self.ui.graphicsView.transform()
        self.currentZoom = transform.m11()

    def treeWidgetChildren(self, item, layer):
        for id in layer._sublayerorder:
            sublayer = layer.sublayers.get(id)
            childItem = QTreeWidgetItem([sublayer.name, "Layer", sublayer.id, layer.id])
            
            if hasattr(self, 'missing_assets') and hasattr(sublayer, '_content') and sublayer._content is not None:
                if hasattr(sublayer, 'content') and hasattr(sublayer.content, 'src'):
                    if sublayer.content.src in self.missing_assets:
                        childItem.setText(0, "⚠️ " + sublayer.name)
                        childItem.setForeground(0, QColor(255, 0, 0))
            
            item.addChild(childItem)

            if len(sublayer._sublayerorder) > 0:
                self.treeWidgetChildren(childItem, sublayer)
            if sublayer._animations is not None:
                for animation in sublayer.animations:
                    animItem = QTreeWidgetItem([animation.keyPath, "Animation", "", sublayer.id])
                    childItem.addChild(animItem)

    def formatFloat(self, value, decimal_places=2):
        try:
            float_val = float(value)
            return f"{float_val:.{decimal_places}f}"
        except (ValueError, TypeError):
            return value

    def formatPoint(self, point_str, decimal_places=2):
        try:
            parts = point_str.split()
            formatted_parts = [self.formatFloat(part, decimal_places) for part in parts]
            return " ".join(formatted_parts)
        except:
            return point_str

    def openInInspector(self, current, _):
        if current is None:
            return
            
        self.currentSelectedItem = current
        self.ui.tableWidget.setRowCount(0)
        row_index = 0
        
        self.ui.tableWidget.insertRow(row_index)
        self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem("name"))
        self.ui.tableWidget.item(row_index, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(current.text(0)))
        row_index += 1
        
        element_type = current.text(1)
        if element_type == "Animation":
            parent = self.cafile.rootlayer.findlayer(current.text(3))
            element = parent.findanimation(current.text(0))
            if element:
                self.add_inspector_row("type", element.type, row_index)
                row_index += 1
                
                self.add_inspector_row("keyPath", element.keyPath, row_index)
                row_index += 1
                
                if hasattr(element, "duration") and element.duration:
                    self.add_inspector_row("duration", self.formatFloat(element.duration), row_index)
                    row_index += 1
                
                if hasattr(element, "beginTime") and element.beginTime:
                    self.add_inspector_row("beginTime", self.formatFloat(element.beginTime), row_index)
                    row_index += 1
                
                if hasattr(element, "fillMode") and element.fillMode:
                    self.add_inspector_row("fillMode", element.fillMode, row_index)
                    row_index += 1
                
                if hasattr(element, "removedOnCompletion") and element.removedOnCompletion:
                    self.add_inspector_row("removedOnCompletion", element.removedOnCompletion, row_index)
                    row_index += 1
                
                if hasattr(element, "repeatCount") and element.repeatCount:
                    self.add_inspector_row("repeatCount", self.formatFloat(element.repeatCount), row_index)
                    row_index += 1
                
                if hasattr(element, "calculationMode") and element.calculationMode:
                    self.add_inspector_row("calculationMode", element.calculationMode, row_index)
                    row_index += 1
                
                if element.type == "CASpringAnimation":
                    if hasattr(element, "damping") and element.damping:
                        self.add_inspector_row("damping", self.formatFloat(element.damping), row_index)
                        row_index += 1
                    
                    if hasattr(element, "mass") and element.mass:
                        self.add_inspector_row("mass", self.formatFloat(element.mass), row_index)
                        row_index += 1
                    
                    if hasattr(element, "stiffness") and element.stiffness:
                        self.add_inspector_row("stiffness", self.formatFloat(element.stiffness), row_index)
                        row_index += 1
                    
                    if hasattr(element, "velocity") and element.velocity:
                        self.add_inspector_row("velocity", self.formatFloat(element.velocity), row_index)
                        row_index += 1
                    
                    if hasattr(element, "mica_autorecalculatesDuration"):
                        self.add_inspector_row("mica_autorecalculatesDuration", 
                                             element.mica_autorecalculatesDuration, row_index)
                        row_index += 1
                
                if element.type == "CAKeyframeAnimation":
                    if hasattr(element, "values") and element.values:
                        values_str = ", ".join([self.formatFloat(value.value) for value in element.values])
                        self.add_inspector_row("values", values_str, row_index)
                        row_index += 1
                    
                    if hasattr(element, "keyTimes") and element.keyTimes:
                        times_str = ", ".join([self.formatFloat(time.value) for time in element.keyTimes])
                        self.add_inspector_row("keyTimes", times_str, row_index)
                        row_index += 1
                
                if element.type == "CAMatchMoveAnimation":
                    if hasattr(element, "additive") and element.additive:
                        self.add_inspector_row("additive", element.additive, row_index)
                        row_index += 1
                    
                    if hasattr(element, "appliesX") and element.appliesX:
                        self.add_inspector_row("appliesX", element.appliesX, row_index)
                        row_index += 1
                    
                    if hasattr(element, "appliesY") and element.appliesY:
                        self.add_inspector_row("appliesY", element.appliesY, row_index)
                        row_index += 1
                    
                    if hasattr(element, "appliesScale") and element.appliesScale:
                        self.add_inspector_row("appliesScale", element.appliesScale, row_index)
                        row_index += 1
                    
                    if hasattr(element, "appliesRotation") and element.appliesRotation:
                        self.add_inspector_row("appliesRotation", element.appliesRotation, row_index)
                        row_index += 1
                
                if element.type == "LKAnimationGroup":
                    if hasattr(element, "animations") and element.animations:
                        self.add_inspector_row("subAnimations", str(len(element.animations)), row_index)
                        row_index += 1
                
                self.highlightAnimationInPreview(parent, element)
                
        elif element_type == "Layer" or element_type == "Root":
            if element_type == "Layer":
                element = self.cafile.rootlayer.findlayer(current.text(2))
            else:
                element = self.cafile.rootlayer
                
            if element:
                self.add_inspector_row("id", element.id, row_index)
                row_index += 1
                
                layer_type = "CALayer"
                if hasattr(element, "layer_class") and element.layer_class:
                    layer_type = element.layer_class
                self.add_inspector_row("class", layer_type, row_index)
                row_index += 1
                
                if hasattr(element, "position") and element.position:
                    pos_str = self.formatPoint(" ".join(element.position))
                    self.add_inspector_row("position", pos_str, row_index)
                    row_index += 1
                
                if hasattr(element, "bounds") and element.bounds:
                    bounds_str = self.formatPoint(" ".join(element.bounds))
                    self.add_inspector_row("bounds", bounds_str, row_index)
                    row_index += 1
                
                if hasattr(element, "frame") and element.frame:
                    frame_str = self.formatPoint(" ".join(element.frame))
                    self.add_inspector_row("frame", frame_str, row_index)
                    row_index += 1
                
                if hasattr(element, "transform") and element.transform:
                    transform_str = self.formatPoint(element.transform)
                    self.add_inspector_row("transform", transform_str, row_index)
                    row_index += 1
                
                if hasattr(element, "anchorPoint") and element.anchorPoint:
                    anchor_str = self.formatPoint(element.anchorPoint)
                    self.add_inspector_row("anchorPoint", anchor_str, row_index)
                    row_index += 1
                
                if hasattr(element, "zPosition") and element.zPosition:
                    self.add_inspector_row("zPosition", self.formatFloat(element.zPosition), row_index)
                    row_index += 1
                
                if hasattr(element, "backgroundColor") and element.backgroundColor:
                    self.add_inspector_row("backgroundColor", element.backgroundColor, row_index)
                    row_index += 1
                
                if hasattr(element, "cornerRadius") and element.cornerRadius:
                    self.add_inspector_row("cornerRadius", self.formatFloat(element.cornerRadius), row_index)
                    row_index += 1
                
                if hasattr(element, "opacity") and element.opacity is not None:
                    self.add_inspector_row("opacity", self.formatFloat(element.opacity), row_index)
                    row_index += 1
                
                if hasattr(element, "mica_animatedAlpha") and element.mica_animatedAlpha is not None:
                    self.add_inspector_row("mica_animatedAlpha", self.formatFloat(element.mica_animatedAlpha), row_index)
                    row_index += 1
                
                if hasattr(element, "geometryFlipped"):
                    self.add_inspector_row("geometryFlipped", str(element.geometryFlipped), row_index)
                    row_index += 1
                
                if hasattr(element, "hidden"):
                    self.add_inspector_row("hidden", str(element.hidden), row_index)
                    row_index += 1
                
                if hasattr(element, "layer_class") and element.layer_class == "CATextLayer":
                    if hasattr(element, "string") and element.string:
                        self.add_inspector_row("string", element.string, row_index)
                        row_index += 1
                    
                    if hasattr(element, "fontSize") and element.fontSize:
                        self.add_inspector_row("fontSize", self.formatFloat(element.fontSize), row_index)
                        row_index += 1
                    
                    if hasattr(element, "fontFamily") and element.fontFamily:
                        self.add_inspector_row("fontFamily", element.fontFamily, row_index)
                        row_index += 1
                    
                    if hasattr(element, "alignmentMode") and element.alignmentMode:
                        self.add_inspector_row("alignmentMode", element.alignmentMode, row_index)
                        row_index += 1
                    
                    if hasattr(element, "color") and element.color:
                        self.add_inspector_row("color", element.color, row_index)
                        row_index += 1
                
                if hasattr(element, "states") and element.states:
                    states_str = ", ".join(element.states.keys())
                    self.add_inspector_row("states", states_str, row_index)
                    row_index += 1
                
                if hasattr(element, "animations") and element.animations:
                    self.add_inspector_row("animationCount", str(len(element.animations)), row_index)
                    row_index += 1
                
                if hasattr(element, "_sublayerorder") and element._sublayerorder:
                    self.add_inspector_row("sublayerCount", str(len(element._sublayerorder)), row_index)
                    row_index += 1
                
                if hasattr(element, "_content") and element._content is not None:
                    if hasattr(element, "content") and isinstance(element.content, object):
                        if hasattr(element.content, "src"):
                            self.add_inspector_row("contentSrc", element.content.src, row_index)
                            row_index += 1
                
                self.highlightLayerInPreview(element)
        
    def add_inspector_row(self, key, value, row_index):
        self.ui.tableWidget.insertRow(row_index)
        key_item = QTableWidgetItem(key)
        key_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(row_index, 0, key_item)
        value_item = QTableWidgetItem(str(value))
        self.ui.tableWidget.setItem(row_index, 1, value_item)
    
    def renderPreview(self, root_layer):
        self.scene.clear()
        
        bounds = QRectF(0, 0, 1000, 1000)
        if hasattr(root_layer, "bounds") and root_layer.bounds:
            try:
                x = float(root_layer.bounds[0])
                y = float(root_layer.bounds[1])
                w = float(root_layer.bounds[2])
                h = float(root_layer.bounds[3])
                bounds = QRectF(x, y, w, h)
            except (ValueError, IndexError):
                pass
        
        border_rect = QGraphicsRectItem(bounds)
        border_rect.setPen(QPen(QColor(0, 0, 0), 2))
        border_rect.setBrush(QBrush(Qt.transparent))
        self.scene.addItem(border_rect)
        
        base_state = None
        if hasattr(root_layer, "states") and root_layer.states and "Base State" in root_layer.states:
            base_state = root_layer.states["Base State"]
        
        root_pos = QPointF(0, 0)
        if hasattr(root_layer, "position") and root_layer.position:
            try:
                root_pos = QPointF(float(root_layer.position[0]), float(root_layer.position[1]))
            except (ValueError, IndexError):
                pass
        
        self.renderLayer(root_layer, root_pos, QTransform(), base_state)
        
        all_items_rect = self.scene.itemsBoundingRect()
        self.scene.setSceneRect(all_items_rect)
    
    def findAssetPath(self, src_path):
        if not src_path:
            return None
        
        try:
            import urllib.parse
            decoded_path = urllib.parse.unquote(src_path)
            if decoded_path != src_path:
                src_path = decoded_path
        except:
            pass
        
        if os.path.isabs(src_path) and os.path.exists(src_path):
            return src_path
        
        base_path = os.path.join(self.cafilepath, src_path)
        if os.path.exists(base_path):
            return base_path
        
        assets_path = os.path.join(self.cafilepath, "assets", os.path.basename(src_path))
        if os.path.exists(assets_path):
            return assets_path
        
        direct_path = os.path.join(self.cafilepath, os.path.basename(src_path))
        if os.path.exists(direct_path):
            return direct_path
        
        parent_path = os.path.join(os.path.dirname(self.cafilepath), os.path.basename(src_path))
        if os.path.exists(parent_path):
            return parent_path
        
        parent_assets_path = os.path.join(os.path.dirname(self.cafilepath), "assets", os.path.basename(src_path))
        if os.path.exists(parent_assets_path):
            return parent_assets_path
        
        filename = os.path.basename(src_path)
        assets_dir = os.path.join(self.cafilepath, "assets")
        if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
            for file in os.listdir(assets_dir):
                if file.lower() == filename.lower():
                    return os.path.join(assets_dir, file)
                
        parent_assets_dir = os.path.join(os.path.dirname(self.cafilepath), "assets")
        if os.path.exists(parent_assets_dir) and os.path.isdir(parent_assets_dir):
            for file in os.listdir(parent_assets_dir):
                if file.lower() == filename.lower():
                    return os.path.join(parent_assets_dir, file)
                
        if os.path.isdir(self.cafilepath):
            for file in os.listdir(self.cafilepath):
                if os.path.isfile(os.path.join(self.cafilepath, file)) and file.lower() == filename.lower():
                    return os.path.join(self.cafilepath, file)
                
        parent_dir = os.path.dirname(self.cafilepath)
        if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
            for file in os.listdir(parent_dir):
                if os.path.isfile(os.path.join(parent_dir, file)) and file.lower() == filename.lower():
                    return os.path.join(parent_dir, file)
        
        return self.findAssetRecursive(self.cafilepath, filename, max_depth=3)
    
    def findAssetRecursive(self, directory, filename, max_depth=3, current_depth=0):
        if current_depth > max_depth or not os.path.exists(directory) or not os.path.isdir(directory):
            return None
        
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            
            if os.path.isfile(full_path) and file.lower() == filename.lower():
                return full_path
            
            if os.path.isdir(full_path):
                result = self.findAssetRecursive(full_path, filename, max_depth, current_depth + 1)
                if result:
                    return result
                
        return None
    
    def loadImage(self, src_path):
        if not src_path:
            return None
        
        if src_path in self.cachedImages:
            return self.cachedImages[src_path]
        
        asset_path = self.findAssetPath(src_path)
        if not asset_path or not os.path.exists(asset_path):
            print(f"Could not find asset: {src_path}")
            
            if not hasattr(self, 'missing_assets'):
                self.missing_assets = set()
            self.missing_assets.add(src_path)
            
            return None
        
        try:
            img = QImage(asset_path)
            if img.isNull():
                print(f"Failed to load image: {asset_path}")
                return None
            
            pixmap = QPixmap.fromImage(img)
            self.cachedImages[src_path] = pixmap
            print(f"Loaded image successfully: {asset_path}")
            return pixmap
        except Exception as e:
            print(f"Error loading image {asset_path}: {e}")
            return None
        
    def parseTransform(self, transform_str):
        transform = QTransform()
        if not transform_str:
            return transform
            
        try:
            if "scale" in transform_str:
                scale_parts = transform_str.split("scale(")[1].split(")")[0].split(",")
                scale_x = float(scale_parts[0].strip())
                scale_y = float(scale_parts[1].strip())
                transform.scale(scale_x, scale_y)
                
            if "rotate" in transform_str:
                rotation_str = transform_str.split("rotate(")[1].split("deg")[0].strip()
                rotation_angle = float(rotation_str)
                transform.rotate(rotation_angle)
                
            if "translate" in transform_str:
                translate_parts = transform_str.split("translate(")[1].split(")")[0].split(",")
                translate_x = float(translate_parts[0].strip())
                translate_y = float(translate_parts[1].strip())
                transform.translate(translate_x, translate_y)
        except:
            pass
            
        return transform
        
    def renderLayer(self, layer, parent_pos, parent_transform, base_state=None, target_state=None):
        if hasattr(layer, "hidden") and layer.hidden:
            return

        absolute_position = QPointF(parent_pos)
        layer_position = QPointF(0, 0)
        
        if hasattr(layer, "position") and layer.position:
            try:
                layer_position = QPointF(float(layer.position[0]), float(layer.position[1]))
            except (ValueError, IndexError):
                pass
        
        bounds = QRectF(0, 0, 100, 100)
        if hasattr(layer, "bounds") and layer.bounds:
            try:
                x = float(layer.bounds[0])
                y = float(layer.bounds[1])
                w = float(layer.bounds[2])
                h = float(layer.bounds[3])
                bounds = QRectF(x, y, w, h)
            except (ValueError, IndexError):
                pass
        
        transform = QTransform(parent_transform)
        if hasattr(layer, "transform") and layer.transform:
            layer_transform = self.parseTransform(layer.transform)
            transform = transform * layer_transform
        
        anchor_point = QPointF(0.5, 0.5)
        if hasattr(layer, "anchorPoint") and layer.anchorPoint:
            try:
                anchor_parts = layer.anchorPoint.split(" ")
                if len(anchor_parts) >= 2:
                    anchor_point = QPointF(float(anchor_parts[0]), float(anchor_parts[1]))
            except:
                pass
        
        z_position = 0
        if hasattr(layer, "zPosition") and layer.zPosition:
            try:
                z_position = float(layer.zPosition)
            except (ValueError, TypeError):
                pass
        
        opacity = 1.0
        if hasattr(layer, "opacity") and layer.opacity is not None:
            try:
                opacity = float(layer.opacity)
            except (ValueError, TypeError):
                pass
        
        background_color = None
        if hasattr(layer, "backgroundColor") and layer.backgroundColor:
            background_color = self.parseColor(layer.backgroundColor)
        
        corner_radius = 0
        if hasattr(layer, "cornerRadius") and layer.cornerRadius:
            try:
                corner_radius = float(layer.cornerRadius)
            except (ValueError, TypeError):
                pass
        
        if base_state and hasattr(base_state, "elements"):
            for element in base_state.elements:
                if element.__class__.__name__ == "LKStateSetValue" and element.targetId == layer.id:
                    if element.keyPath == "position.x" and element.value:
                        try:
                            layer_position.setX(float(element.value))
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "position.y" and element.value:
                        try:
                            layer_position.setY(float(element.value))
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "transform" and element.value:
                        transform = self.parseTransform(element.value) * parent_transform
                    elif element.keyPath == "opacity" and element.value:
                        try:
                            opacity = float(element.value)
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "zPosition" and element.value:
                        try:
                            z_position = float(element.value)
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "backgroundColor" and element.value:
                        background_color = self.parseColor(element.value)
                    elif element.keyPath == "cornerRadius" and element.value:
                        try:
                            corner_radius = float(element.value)
                        except (ValueError, TypeError):
                            pass
        
        if target_state and hasattr(target_state, "elements"):
            for element in target_state.elements:
                if element.__class__.__name__ == "LKStateSetValue" and element.targetId == layer.id:
                    if element.keyPath == "position.x" and element.value:
                        try:
                            layer_position.setX(float(element.value))
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "position.y" and element.value:
                        try:
                            layer_position.setY(float(element.value))
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "transform" and element.value:
                        transform = self.parseTransform(element.value) * parent_transform
                    elif element.keyPath == "opacity" and element.value:
                        try:
                            opacity = float(element.value)
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "zPosition" and element.value:
                        try:
                            z_position = float(element.value)
                        except (ValueError, TypeError):
                            pass
                    elif element.keyPath == "backgroundColor" and element.value:
                        background_color = self.parseColor(element.value)
                    elif element.keyPath == "cornerRadius" and element.value:
                        try:
                            corner_radius = float(element.value)
                        except (ValueError, TypeError):
                            pass
        
        has_content = False
        missing_asset = False
        
        is_text_layer = hasattr(layer, "layer_class") and layer.layer_class == "CATextLayer"
        
        if is_text_layer:
            text_item = QGraphicsTextItem()
            text = layer.string if hasattr(layer, "string") and layer.string else "Text Layer"
            text_item.setPlainText(text)
            
            if hasattr(layer, "fontSize") and layer.fontSize:
                try:
                    font = text_item.font()
                    font_size = float(layer.fontSize)
                    font.setPointSizeF(font_size)
                    text_item.setFont(font)
                except (ValueError, TypeError):
                    pass
            
            if hasattr(layer, "fontFamily") and layer.fontFamily:
                font = text_item.font()
                font.setFamily(layer.fontFamily)
                text_item.setFont(font)
            
            if hasattr(layer, "color") and layer.color:
                color = self.parseColor(layer.color)
                if color:
                    text_item.setDefaultTextColor(color)
            
            text_item.setTransformOriginPoint(bounds.width() * anchor_point.x(),
                                         bounds.height() * anchor_point.y())
            pos_x = layer_position.x() - bounds.width() * anchor_point.x()
            pos_y = layer_position.y() - bounds.height() * anchor_point.y()
            text_item.setPos(pos_x, pos_y)
            text_item.setTransform(transform)
            text_item.setZValue(z_position)
            text_item.setOpacity(opacity)
            
            text_item.setData(0, layer.id)
            text_item.setData(1, "Layer")
            self.scene.addItem(text_item)
            has_content = True
            
            self.applyDefaultAnimationsToLayer(layer, text_item)
            
        elif hasattr(layer, "_content") and layer._content is not None:
            if hasattr(layer, "content") and hasattr(layer.content, "src"):
                src_path = layer.content.src
                pixmap = self.loadImage(src_path)
                
                if not pixmap and hasattr(self, 'missing_assets') and src_path in self.missing_assets:
                    missing_asset = True
                    
                if pixmap:
                    pixmap_item = QGraphicsPixmapItem()
                    pixmap_item.setPixmap(pixmap)

                    scale_factor = 1.0
                    if pixmap.width() > bounds.width() or pixmap.height() > bounds.height():
                        scale_x = bounds.width() / pixmap.width() if pixmap.width() > 0 else 1.0
                        scale_y = bounds.height() / pixmap.height() if pixmap.height() > 0 else 1.0
                        scale_factor = min(scale_x, scale_y)

                    item_transform = QTransform()
                    item_transform.scale(scale_factor, scale_factor)
                    pixmap_item.setTransform(item_transform * transform)

                    scaled_width = pixmap.width() * scale_factor
                    scaled_height = pixmap.height() * scale_factor
                    pixmap_item.setTransformOriginPoint(scaled_width * anchor_point.x(),
                                                        scaled_height * anchor_point.y())

                    pos_x = layer_position.x() - scaled_width * anchor_point.x()
                    pos_y = layer_position.y() - scaled_height * anchor_point.y()
                    pixmap_item.setPos(pos_x, pos_y)

                    pixmap_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
                    pixmap_item.setZValue(z_position)
                    pixmap_item.setOpacity(opacity)
                    pixmap_item.setData(0, layer.id)
                    pixmap_item.setData(1, "Layer")
                    self.scene.addItem(pixmap_item)
                    has_content = True
                    
                    self.applyDefaultAnimationsToLayer(layer, pixmap_item)
        
        if not has_content:
            rect_item = QGraphicsRectItem()
            rect_item.setRect(bounds)
            rect_item.setTransformOriginPoint(bounds.width() * anchor_point.x(),
                                             bounds.height() * anchor_point.y())
            
            pos_x = layer_position.x() - bounds.width() * anchor_point.x()
            pos_y = layer_position.y() - bounds.height() * anchor_point.y()
            
            rect_item.setPos(pos_x, pos_y)
            rect_item.setTransform(transform)
            rect_item.setZValue(z_position)
            rect_item.setOpacity(opacity)
            
            pen = QPen(QColor(200, 200, 200, 180), 1.0)
            brush = QBrush(QColor(180, 180, 180, 30))
            
            if layer.id == self.cafile.rootlayer.id:
                pen = QPen(QColor(0, 0, 0, 200), 1.5)
                brush = QBrush(Qt.transparent)
            
            if missing_asset:
                pen = QPen(QColor(255, 0, 0, 200), 2.0)
                brush = QBrush(QColor(255, 200, 200, 30))
            
            if background_color:
                brush = QBrush(background_color)
            
            if corner_radius > 0:
                pen.setStyle(Qt.PenStyle.DashLine)
            
            rect_item.setPen(pen)
            rect_item.setBrush(brush)
            rect_item.setData(0, layer.id)
            rect_item.setData(1, "Layer")
            self.scene.addItem(rect_item)
            
            self.applyDefaultAnimationsToLayer(layer, rect_item)
            
            if layer.id != self.cafile.rootlayer.id:
                name_item = QGraphicsTextItem(layer.name)
                name_item.setPos(rect_item.pos() + QPointF(5, 5))
                name_item.setDefaultTextColor(QColor(60, 60, 60))
                name_item.setData(0, layer.id + "_name")
                name_item.setTransform(transform)
                name_item.setZValue(z_position + 0.1)
                self.scene.addItem(name_item)
        
        if hasattr(layer, "_sublayerorder") and layer._sublayerorder:
            for layer_id in layer._sublayerorder:
                sublayer = layer.sublayers.get(layer_id)
                if sublayer:
                    self.renderLayer(sublayer, layer_position, transform, base_state, target_state)
    
    def applyDefaultAnimationsToLayer(self, layer, item):
        if not hasattr(layer, "animations") or not layer.animations:
            return
            
        for animation in layer.animations:
            if animation.type == "CAKeyframeAnimation":
                self.applyKeyframeAnimationToItem(item, animation.keyPath, animation)
    
    def highlightLayerInPreview(self, layer):
        self.scene.clearSelection()
        for item in self.scene.items():
            if hasattr(item, "data") and item.data(0) == layer.id and item.data(1) == "Layer":
                if isinstance(item, QGraphicsRectItem):
                    if layer.id == self.cafile.rootlayer.id:
                        item.setPen(QPen(QColor(0, 120, 215, 255), 2))
                    else:
                        item.setPen(QPen(QColor(0, 120, 215, 200), 1.5))
                    item.setSelected(True)
                    self.ui.graphicsView.centerOn(item)
                
        for item in self.scene.items():
            if hasattr(item, "data") and item.data(0) == layer.id + "_name":
                item.setDefaultTextColor(QColor(0, 120, 215))
    
    def highlightAnimationInPreview(self, layer, animation):
        self.highlightLayerInPreview(layer)

    def populateStatesTreeWidget(self):
        if not hasattr(self, 'cafile') or not self.cafile:
            return
            
        self.ui.statesTreeWidget.clear()
        
        self.processStatesInLayer(self.cafile.rootlayer, None)
        
        self.ui.statesTreeWidget.expandAll()
    
    def processStatesInLayer(self, layer, parentItem):
        if not hasattr(layer, "states") or not layer.states:
            return
            
        layerItem = None
        if len(layer.states) > 0:
            if parentItem is None:
                layerName = layer.name if hasattr(layer, "name") else "Root Layer"
                layerItem = QTreeWidgetItem([f"{layerName} States", "LayerFolder", ""])
                self.ui.statesTreeWidget.addTopLevelItem(layerItem)
            else:
                layerName = layer.name if hasattr(layer, "name") else "Sublayer"
                layerItem = QTreeWidgetItem([f"{layerName} States", "LayerFolder", ""])
                parentItem.addChild(layerItem)
                
            for state_name, state in layer.states.items():
                stateItem = QTreeWidgetItem([state_name, "State", layer.id])
                layerItem.addChild(stateItem)
                
                if hasattr(state, "elements") and state.elements:
                    for element in state.elements:
                        if element.__class__.__name__ == "LKStateSetValue":
                            setValue = QTreeWidgetItem([
                                f"{element.keyPath}",
                                "SetValue",
                                f"{element.value} ({element.valueType})"
                            ])
                            setValue.setData(0, QtCore.Qt.UserRole, element.targetId)
                            stateItem.addChild(setValue)
                        elif element.__class__.__name__ == "LKStateAddAnimation":
                            animItem = QTreeWidgetItem([
                                f"{element.keyPath}",
                                "AddAnimation",
                                element.targetId
                            ])
                            stateItem.addChild(animItem)
                            
                            if hasattr(element, "animations") and element.animations:
                                for anim in element.animations:
                                    animType = anim.type if hasattr(anim, "type") else "Unknown"
                                    animDetails = QTreeWidgetItem([
                                        f"{animType}",
                                        "Animation",
                                        f"duration: {anim.duration if hasattr(anim, 'duration') else 'N/A'}"
                                    ])
                                    animItem.addChild(animDetails)
                
                if hasattr(layer, "stateTransitions"):
                    related_transitions = []
                    for transition in layer.stateTransitions:
                        fromState = transition.fromState if hasattr(transition, "fromState") else ""
                        toState = transition.toState if hasattr(transition, "toState") else ""
                        
                        if (fromState == state_name or fromState == "*") or (toState == state_name):
                            related_transitions.append(transition)
                    
                    if related_transitions:
                        transitionsFolder = QTreeWidgetItem([
                            "State Transitions",
                            "TransitionsFolder",
                            ""
                        ])
                        stateItem.addChild(transitionsFolder)
                        
                        for transition in related_transitions:
                            fromState = transition.fromState if hasattr(transition, "fromState") else "*"
                            toState = transition.toState if hasattr(transition, "toState") else "*"
                            
                            direction = "to" if toState == state_name else "from"
                            other_state = fromState if direction == "to" else toState
                            if other_state == "*":
                                other_state = "any state"
                                
                            transitionItem = QTreeWidgetItem([
                                f"{direction} {other_state}",
                                "Transition",
                                layer.id
                            ])
                            transitionItem.setData(0, QtCore.Qt.UserRole, (fromState, toState))
                            transitionsFolder.addChild(transitionItem)
                            
                            if hasattr(transition, "elements") and transition.elements:
                                for element in transition.elements:
                                    if hasattr(element, "targetId") and hasattr(element, "key"):
                                        transElementItem = QTreeWidgetItem([
                                            f"{element.key}",
                                            "TransitionElement",
                                            element.targetId
                                        ])
                                        transitionItem.addChild(transElementItem)
                                        
                                        if hasattr(element, "animations") and element.animations:
                                            for anim in element.animations:
                                                if anim.type == "CASpringAnimation":
                                                    springDetails = f"d:{anim.damping if hasattr(anim, 'damping') else 'N/A'}, m:{anim.mass if hasattr(anim, 'mass') else 'N/A'}, s:{anim.stiffness if hasattr(anim, 'stiffness') else 'N/A'}"
                                                    animItem = QTreeWidgetItem([
                                                        f"{anim.type}",
                                                        "Animation",
                                                        springDetails
                                                    ])
                                                    transElementItem.addChild(animItem)
        
        if hasattr(layer, "sublayers") and layer.sublayers:
            for layer_id in layer._sublayerorder:
                sublayer = layer.sublayers.get(layer_id)
                if sublayer:
                    self.processStatesInLayer(sublayer, layerItem if layerItem else parentItem)
    
    def openStateInInspector(self, current, _):
        if current is None:
            return
            
        self.currentSelectedItem = current
        self.ui.tableWidget.setRowCount(0)
        row_index = 0
        
        self.ui.tableWidget.insertRow(row_index)
        self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem("name"))
        self.ui.tableWidget.item(row_index, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(current.text(0)))
        row_index += 1
        
        element_type = current.text(1)
        self.ui.tableWidget.insertRow(row_index)
        self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem("type"))
        self.ui.tableWidget.item(row_index, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(element_type))
        row_index += 1
        
        if element_type == "State":
            layer_id = current.text(2)
            if layer_id:
                self.add_inspector_row("layerId", layer_id, row_index)
                row_index += 1
            
            current.setData(0, QtCore.Qt.UserRole, layer_id)
            
            state_name = current.text(0)
            layer = None
            
            if layer_id:
                layer = self.cafile.rootlayer.findlayer(layer_id)
            else:
                layer = self.cafile.rootlayer
            
            if layer and hasattr(layer, "states") and state_name in layer.states:
                state = layer.states[state_name]
                
                if hasattr(state, "elements"):
                    self.add_inspector_row("elementCount", str(len(state.elements)), row_index)
                    row_index += 1
                
                self.animations = []
                
                self.previewState(layer, state_name)
                
                was_playing = hasattr(self, 'animations_playing') and self.animations_playing
                if was_playing:
                    self.animations_playing = False
                    self.toggleAnimations()
                
        elif element_type == "Transition":
            parent = current.parent()
            if parent and parent.parent():
                state_item = parent.parent()
                layer_id = state_item.text(2)
                
                transition_data = current.data(0, QtCore.Qt.UserRole)
                if transition_data:
                    fromState, toState = transition_data
                else:
                    direction_parts = current.text(0).split(" ")
                    direction = direction_parts[0]
                    other_state = " ".join(direction_parts[1:])
                    
                    if other_state == "any state":
                        other_state = "*"
                        
                    state_name = state_item.text(0)
                    
                    if direction == "from":
                        fromState = state_name
                        toState = other_state
                    else:
                        fromState = other_state
                        toState = state_name
                
                self.add_inspector_row("fromState", fromState, row_index)
                row_index += 1
                self.add_inspector_row("toState", toState, row_index)
                row_index += 1
                
                if layer_id:
                    self.add_inspector_row("layerId", layer_id, row_index)
                    row_index += 1
                
                self.animations = []
                
                self.previewTransition(layer_id, fromState, toState)
                
                was_playing = hasattr(self, 'animations_playing') and self.animations_playing
                if was_playing:
                    self.animations_playing = False
                    self.toggleAnimations()
                
        elif element_type == "SetValue":
            targetId = current.data(0, QtCore.Qt.UserRole)
            if targetId:
                self.add_inspector_row("targetId", targetId, row_index)
                row_index += 1
                
            keyPath = current.text(0)
            if keyPath:
                self.add_inspector_row("keyPath", keyPath, row_index)
                row_index += 1
                
            value = current.text(2)
            if value:
                self.add_inspector_row("value", value, row_index)
                row_index += 1
                
        elif element_type == "Animation" or element_type == "AddAnimation":
            if element_type == "AddAnimation":
                targetId = current.text(2)
                if targetId:
                    self.add_inspector_row("targetId", targetId, row_index)
                    row_index += 1
                    
                keyPath = current.text(0)
                if keyPath:
                    self.add_inspector_row("keyPath", keyPath, row_index)
                    row_index += 1
            else:
                details = current.text(2)
                if details:
                    for detail in details.split(", "):
                        if ":" in detail:
                            key, value = detail.split(":", 1)
                            self.add_inspector_row(key.strip(), value.strip(), row_index)
                            row_index += 1
        
        elif element_type == "TransitionElement":
            key = current.text(0)
            if key:
                self.add_inspector_row("key", key, row_index)
                row_index += 1
                
            targetId = current.text(2)
            if targetId:
                self.add_inspector_row("targetId", targetId, row_index)
                row_index += 1
    
    def previewState(self, layer, state_name):
        if not layer or not state_name:
            return
            
        self.scene.clear()
        
        base_state = None
        if hasattr(layer, "states") and "Base State" in layer.states:
            base_state = layer.states["Base State"]
            
        target_state = None
        if hasattr(layer, "states") and state_name in layer.states:
            target_state = layer.states[state_name]
        
        self.renderPreview(layer, target_state)
        
        if target_state and hasattr(target_state, "elements"):
            for element in target_state.elements:
                if element.__class__.__name__ == "LKStateAddAnimation":
                    self.applyAnimationsToPreview(element)
                    
    def previewTransition(self, layer_id, fromState, toState):
        layer = None
        if layer_id:
            layer = self.cafile.rootlayer.findlayer(layer_id)
        else:
            layer = self.cafile.rootlayer
            
        if not layer:
            return
            
        self.previewState(layer, fromState if fromState != "*" else "Base State")
        
        transition = None
        if hasattr(layer, "stateTransitions"):
            for t in layer.stateTransitions:
                if (t.fromState == fromState or t.fromState == "*") and t.toState == toState:
                    transition = t
                    break
                    
        if not transition:
            return
            
        if hasattr(transition, "elements"):
            for element in transition.elements:
                if hasattr(element, "animations"):
                    for anim in element.animations:
                        self.applyTransitionAnimationToPreview(element.targetId, element.key, anim)
                        
    def applyAnimationsToPreview(self, animation_element):
        targetId = animation_element.targetId
        
        if not hasattr(animation_element, "keyPath"):
            print("Warning: animation_element missing keyPath attribute")
            return
            
        keyPath = animation_element.keyPath
        
        if not isinstance(keyPath, str):
            print(f"Warning: keyPath is not a string: {type(keyPath)}")
            return
            
        for item in self.scene.items():
            if hasattr(item, "data") and item.data(0) == targetId:
                if hasattr(animation_element, "animations"):
                    for anim in animation_element.animations:
                        if anim.type == "CAKeyframeAnimation":
                            self.applyKeyframeAnimationToItem(item, keyPath, anim)
                
    def applyKeyframeAnimationToItem(self, item, keyPath, anim):
        if not isinstance(keyPath, str):
            print(f"Warning: keyPath is not a string: {type(keyPath)}")
            return
            
        animation = QVariantAnimation()
        
        try:
            if hasattr(anim, "duration"):
                if isinstance(anim.duration, (int, float)):
                    duration_ms = int(float(anim.duration) * 1000)
                else:
                    duration_ms = int(float(anim.duration) * 1000)
            else:
                duration_ms = 1000
                
            animation.setDuration(duration_ms)
        except (ValueError, TypeError) as e:
            print(f"Error setting animation duration: {e}")
            animation.setDuration(1000)
            
        if hasattr(anim, "keyTimes") and anim.keyTimes and hasattr(anim, "values") and anim.values:
            keyframes = []
            
            for i, keyTime in enumerate(anim.keyTimes):
                if i < len(anim.values):
                    try:
                        time_pct = 0
                        if hasattr(keyTime, 'value') and keyTime.value is not None:
                            time_pct = float(keyTime.value)
                        
                        value_obj = anim.values[i]
                        anim_value = 0
                        if hasattr(value_obj, 'value') and value_obj.value is not None:
                            anim_value = float(value_obj.value)
                            
                        keyframes.append((time_pct, anim_value))
                    except (ValueError, TypeError) as e:
                        print(f"Error parsing keyframe: {e}")
                    
            if "position.x" in keyPath:
                animation.setStartValue(item.x())
                for time_pct, value in keyframes:
                    try:
                        animation.setKeyValueAt(time_pct, value)
                    except (ValueError, TypeError) as e:
                        print(f"Error setting keyframe at {time_pct} with value {value}: {e}")
                
                if keyframes:
                    animation.setEndValue(keyframes[-1][1])
                
                def updatePosX(value):
                    item.setX(value)
                
                animation.valueChanged.connect(updatePosX)
                
            elif "position.y" in keyPath:
                animation.setStartValue(item.y())
                for time_pct, value in keyframes:
                    try:
                        animation.setKeyValueAt(time_pct, value)
                    except (ValueError, TypeError) as e:
                        print(f"Error setting keyframe at {time_pct} with value {value}: {e}")
                
                if keyframes:
                    animation.setEndValue(keyframes[-1][1])
                
                def updatePosY(value):
                    item.setY(value)
                
                animation.valueChanged.connect(updatePosY)
        
        if hasattr(self, 'animations_playing') and self.animations_playing:
            animation.start()
        
        if not hasattr(self, 'animations'):
            self.animations = []
            
        if hasattr(animation, 'duration') and animation.duration() > 0:
            self.animations.append((animation, anim))
        
    def applyTransitionAnimationToPreview(self, targetId, keyPath, animation):
        if not isinstance(keyPath, str):
            print(f"Warning: keyPath is not a string: {type(keyPath)}")
            return
            
        for item in self.scene.items():
            if hasattr(item, "data") and item.data(0) == targetId:
                if animation.type == "CASpringAnimation":
                    self.applySpringAnimationToItem(item, keyPath, animation)
                    
    def applySpringAnimationToItem(self, item, keyPath, animation):
        damping = 10.0
        mass = 1.0
        stiffness = 100.0
        velocity = 0.0
        duration = 0.8
        
        if hasattr(animation, "damping"):
            try:
                damping = float(animation.damping)
            except (ValueError, TypeError):
                pass
                
        if hasattr(animation, "mass"):
            try:
                mass = float(animation.mass)
            except (ValueError, TypeError):
                pass
                
        if hasattr(animation, "stiffness"):
            try:
                stiffness = float(animation.stiffness)
            except (ValueError, TypeError):
                pass
                
        if hasattr(animation, "velocity"):
            try:
                velocity = float(animation.velocity)
            except (ValueError, TypeError):
                pass
                
        if hasattr(animation, "duration"):
            try:
                duration = float(animation.duration)
            except (ValueError, TypeError):
                pass
                
        timeline = QtCore.QTimeLine(int(duration * 1000))
        timeline.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        timeline.setLoopCount(1)
        
        animation_obj = QGraphicsItemAnimation()
        animation_obj.setItem(item)
        animation_obj.setTimeLine(timeline)
        
        if "position.y" in keyPath:
            current_y = item.pos().y()
            target_y = current_y + 50
            animation_obj.setPosAt(0.0, QPointF(item.pos().x(), current_y))
            animation_obj.setPosAt(1.0, QPointF(item.pos().x(), target_y))
        elif "position.x" in keyPath:
            current_x = item.pos().x()
            target_x = current_x + 50
            animation_obj.setPosAt(0.0, QPointF(current_x, item.pos().y()))
            animation_obj.setPosAt(1.0, QPointF(target_x, item.pos().y()))
        elif "opacity" in keyPath:
            pass
        
        if hasattr(self, 'animations_playing') and self.animations_playing:
            timeline.start()
        
        if not hasattr(self, 'animations'):
            self.animations = []
        self.animations.append((timeline, animation))

    def toggleAnimations(self):
        if not hasattr(self, 'animations_playing'):
            self.animations_playing = False
            
        self.animations_playing = not self.animations_playing
        
        if self.animations_playing:
            self.playButton.setIcon(self.pauseIcon)
            for anim, _ in self.animations:
                if isinstance(anim, QVariantAnimation):
                    if anim.state() == QVariantAnimation.State.Stopped:
                        anim.start()
                    else:
                        anim.resume()
                elif isinstance(anim, QtCore.QTimeLine):
                    if anim.state() == QtCore.QTimeLine.State.NotRunning:
                        anim.start()
                    else:
                        anim.resume()
        else:
            self.playButton.setIcon(self.playIcon)
            for anim, _ in self.animations:
                if isinstance(anim, QVariantAnimation):
                    anim.pause()
                elif isinstance(anim, QtCore.QTimeLine):
                    anim.setPaused(True)
                    
    def renderPreview(self, root_layer, target_state=None):
        self.scene.clear()
        
        bounds = QRectF(0, 0, 1000, 1000)
        if hasattr(root_layer, "bounds") and root_layer.bounds:
            try:
                x = float(root_layer.bounds[0])
                y = float(root_layer.bounds[1])
                w = float(root_layer.bounds[2])
                h = float(root_layer.bounds[3])
                bounds = QRectF(x, y, w, h)
            except (ValueError, IndexError):
                pass
        
        border_rect = QGraphicsRectItem(bounds)
        border_rect.setPen(QPen(QColor(0, 0, 0), 2))
        border_rect.setBrush(QBrush(Qt.transparent))
        self.scene.addItem(border_rect)
        
        base_state = None
        if hasattr(root_layer, "states") and root_layer.states and "Base State" in root_layer.states:
            base_state = root_layer.states["Base State"]
        
        root_pos = QPointF(0, 0)
        if hasattr(root_layer, "position") and root_layer.position:
            try:
                root_pos = QPointF(float(root_layer.position[0]), float(root_layer.position[1]))
            except (ValueError, IndexError):
                pass
        
        self.renderLayer(root_layer, root_pos, QTransform(), base_state, target_state)
        
        all_items_rect = self.scene.itemsBoundingRect()
        self.scene.setSceneRect(all_items_rect)

    def parseColor(self, color_str):
        if not color_str:
            return None
            
        try:
            if color_str.lower() in ["black", "white", "red", "green", "blue", "yellow"]:
                return QColor(color_str)
                
            if color_str.startswith("rgb("):
                rgb = color_str.replace("rgb(", "").replace(")", "").split(",")
                if len(rgb) >= 3:
                    r = int(rgb[0].strip())
                    g = int(rgb[1].strip())
                    b = int(rgb[2].strip())
                    return QColor(r, g, b)
                    
            if color_str.startswith("rgba("):
                rgba = color_str.replace("rgba(", "").replace(")", "").split(",")
                if len(rgba) >= 4:
                    r = int(rgba[0].strip())
                    g = int(rgba[1].strip())
                    b = int(rgba[2].strip())
                    a = int(float(rgba[3].strip()) * 255)
                    return QColor(r, g, b, a)
                    
            if color_str.startswith("#"):
                return QColor(color_str)
        except:
            pass
            
        return QColor(150, 150, 150, 100)
