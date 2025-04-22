import sys
import os
import math
from lib.main.main import CAFile
from PySide6 import QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSize, QEvent
from PySide6.QtGui import QPixmap, QImage, QBrush, QPen, QColor, QTransform, QPainter, QLinearGradient
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMainWindow, QTableWidgetItem, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsTextItem, QApplication, QGraphicsView
from ui.ui_mainwindow import Ui_OpenPoster


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
    def __init__(self, parent=None, min_zoom=0.1, max_zoom=10.0):
        super(CustomGraphicsView, self).__init__(parent)
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._last_mouse_pos = QPointF()
        self.setMouseTracking(True)
        self._panning = False
        self.minZoom = min_zoom
        self.maxZoom = max_zoom
    
    def wheelEvent(self, event):
        if event.phase() == Qt.ScrollPhase.ScrollBegin:
            self._pinch_start_zoom = 1.0 
        
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers == Qt.KeyboardModifier.ControlModifier or event.pixelDelta().x() != 0:
            delta = event.angleDelta().y() / 120.0
            current_scale = self.transform().m11()

            zoom_increment = 1.15

            if delta > 0:
                potential_scale = current_scale * zoom_increment
                new_scale = min(potential_scale, self.maxZoom)
            else:
                potential_scale = current_scale / zoom_increment
                new_scale = max(potential_scale, self.minZoom)

            scale_factor = 1.0
            if abs(current_scale) > 1e-9:
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_OpenPoster()
        self.ui.setupUi(self)
        
        view_geometry = self.ui.graphicsView.geometry()
        self.custom_view = CustomGraphicsView(
            parent=self.ui.previewWidget, 
            min_zoom=0.1, 
            max_zoom=10.0
        )
        self.custom_view.setObjectName("graphicsView")
        self.custom_view.setGeometry(view_geometry)
        self.ui.previewLayout.replaceWidget(self.ui.graphicsView, self.custom_view)
        self.ui.graphicsView = self.custom_view
        
        self.ui.openFile.clicked.connect(self.openFile)
        self.ui.treeWidget.currentItemChanged.connect(self.openInInspector)
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
            
            self.scene.clear()
            self.currentZoom = 1.0
            self.ui.graphicsView.resetTransform()
            self.renderPreview(self.cafile.rootlayer)
            self.fitPreviewToView()
        else:
            self.ui.filename.setText("No File Open")
            self.ui.filename.setStyleSheet("border: 1.5px solid palette(highlight); border-radius: 8px; padding: 5px 10px; color: #666666; font-style: italic;")

    def fitPreviewToView(self):
        self.ui.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
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
                
                self.highlightAnimationInPreview(parent, element)
                
        elif element_type == "Layer" or element_type == "Root":
            if element_type == "Layer":
                element = self.cafile.rootlayer.findlayer(current.text(2))
            else:
                element = self.cafile.rootlayer
                
            if element:
                self.add_inspector_row("id", element.id, row_index)
                row_index += 1
                
                if hasattr(element, "position") and element.position:
                    pos_str = self.formatPoint(" ".join(element.position))
                    self.add_inspector_row("position", pos_str, row_index)
                    row_index += 1
                
                if hasattr(element, "bounds") and element.bounds:
                    bounds_str = self.formatPoint(" ".join(element.bounds))
                    self.add_inspector_row("bounds", bounds_str, row_index)
                    row_index += 1
                
                if hasattr(element, "transform") and element.transform:
                    transform_str = self.formatPoint(element.transform)
                    self.add_inspector_row("transform", transform_str, row_index)
                    row_index += 1
                
                if hasattr(element, "anchorPoint") and element.anchorPoint:
                    anchor_str = self.formatPoint(element.anchorPoint)
                    self.add_inspector_row("anchorPoint", anchor_str, row_index)
                    row_index += 1
                
                if hasattr(element, "geometryFlipped"):
                    self.add_inspector_row("geometryFlipped", str(element.geometryFlipped), row_index)
                    row_index += 1
                
                if hasattr(element, "hidden"):
                    self.add_inspector_row("hidden", str(element.hidden), row_index)
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
        
        self.scene.setSceneRect(bounds)
    
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
        
    def renderLayer(self, layer, parent_pos, parent_transform, base_state=None):
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
        
        has_content = False
        missing_asset = False
        
        if hasattr(layer, "_content") and layer._content is not None:
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
                    pixmap_item.setData(0, layer.id)
                    pixmap_item.setData(1, "Layer")
                    self.scene.addItem(pixmap_item)
                    has_content = True
        
        if not has_content:
            rect_item = QGraphicsRectItem()
            rect_item.setRect(bounds)
            rect_item.setTransformOriginPoint(bounds.width() * anchor_point.x(),
                                             bounds.height() * anchor_point.y())
            
            pos_x = layer_position.x() - bounds.width() * anchor_point.x()
            pos_y = layer_position.y() - bounds.height() * anchor_point.y()
            
            rect_item.setPos(pos_x, pos_y)
            rect_item.setTransform(transform)
            
            pen = QPen(QColor(200, 200, 200, 180), 1.0)
            brush = QBrush(QColor(180, 180, 180, 30))
            
            if layer.id == self.cafile.rootlayer.id:
                pen = QPen(QColor(0, 0, 0, 200), 1.5)
                brush = QBrush(Qt.transparent)
            
            if missing_asset:
                pen = QPen(QColor(255, 0, 0, 200), 2.0)
                brush = QBrush(QColor(255, 200, 200, 30))
            
            rect_item.setPen(pen)
            rect_item.setBrush(brush)
            rect_item.setData(0, layer.id)
            rect_item.setData(1, "Layer")
            self.scene.addItem(rect_item)
            
            if layer.id != self.cafile.rootlayer.id:
                name_item = QGraphicsTextItem(layer.name)
                name_item.setPos(rect_item.pos() + QPointF(5, 5))
                name_item.setDefaultTextColor(QColor(60, 60, 60))
                name_item.setData(0, layer.id + "_name")
                name_item.setTransform(transform)
                self.scene.addItem(name_item)
        
        if hasattr(layer, "_sublayerorder") and layer._sublayerorder:
            for layer_id in layer._sublayerorder:
                sublayer = layer.sublayers.get(layer_id)
                if sublayer:
                    self.renderLayer(sublayer, layer_position, transform, base_state)
    
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
