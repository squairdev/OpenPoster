from PySide6.QtGui import QColor, QPen, QBrush, QTransform, QPixmap
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsTextItem, QApplication
from PySide6.QtCore import Qt, QPointF, QRectF, QVariantAnimation
import os

class PreviewRenderingMixin:
    def renderPreview(self, root_layer, target_state=None):
        if hasattr(self._applyAnimation, 'animations'):
            self._applyAnimation.animations.clear()
        self.animations = []
        self.scene.clear()
        
        self.renderLayer(root_layer, QPointF(0,0), QTransform(), target_state=target_state)

    def renderLayer(self, layer, parent_pos, parent_transform, base_state=None, target_state=None):
        if hasattr(layer, 'hidden') and layer.hidden:
            return

        x, y, w, h = [float(p) for p in layer.bounds]
        pos_x, pos_y = [float(p) for p in layer.position] if hasattr(layer, 'position') else [0, 0]
        
        item_pos = QPointF(pos_x, pos_y)
        
        item = None

        if hasattr(layer, 'content') and layer.content and hasattr(layer.content, 'src'):
            pixmap = self.getPixmapForLayer(layer)
            if pixmap:
                item = QGraphicsPixmapItem(pixmap)
        elif hasattr(layer, 'layer_class') and layer.layer_class == "CATextLayer" and hasattr(layer, 'string'):
            item = QGraphicsTextItem(layer.string)
        else:
            item = QGraphicsRectItem(0, 0, w, h)
            
        if item is not None:
            self.scene.addItem(item)
            item.setPos(item_pos)
            item.setData(0, layer.id)
            item.setData(1, "Layer")
            
        self.applyStylesToItem(item, layer)

        if hasattr(layer, "animations") and not target_state:
            self.applyDefaultAnimationsToLayer(layer)

        if hasattr(layer, "sublayers") and layer.sublayers and hasattr(layer, '_sublayerorder'):
            for sublayer_id in layer._sublayerorder:
                sublayer = layer.sublayers.get(sublayer_id)
                if sublayer:
                    self.renderLayer(sublayer, item_pos, item.transform(), base_state, target_state)

        if target_state:
            self.applyStateToLayer(layer, item, target_state)

    def applyStylesToItem(self, item, layer):
        if item is None:
            return

        is_root = (layer == self.cafile.rootlayer)

        x, y, w, h = [float(p) for p in layer.bounds]
        item.setRect(0, 0, w, h) if isinstance(item, QGraphicsRectItem) else None

        if hasattr(layer, 'backgroundColor'):
            color = self.parseColor(layer.backgroundColor)
            if color:
                if isinstance(item, QGraphicsRectItem):
                    item.setBrush(QBrush(color))
                    if not is_root:
                        item.setPen(QPen(Qt.NoPen))
                elif isinstance(item, QGraphicsTextItem):
                    item.setDefaultTextColor(color)
            else:
                if isinstance(item, QGraphicsRectItem):
                    item.setBrush(QBrush(QColor(0,0,0,0)))
                    if not is_root:
                        item.setPen(QPen(Qt.NoPen))
        
        if is_root and isinstance(item, QGraphicsRectItem):
            pen = QPen(QColor(128, 128, 128), 2, Qt.DashLine)
            item.setPen(pen)

        if hasattr(layer, 'opacity') and layer.opacity is not None:
            item.setOpacity(float(layer.opacity))

    def getPixmapForLayer(self, layer):
        src_path = self.findAssetPath(layer.content.src)
        if src_path in self.cachedImages:
            return self.cachedImages[src_path]
        
        if src_path and os.path.exists(src_path):
            pixmap = QPixmap(src_path)
            self.cachedImages[src_path] = pixmap
            return pixmap
        else:
            self.missing_assets.add(layer.content.src)
            return None

    def applyDefaultAnimationsToLayer(self, layer):
        self.applyAnimationsToPreview(layer)

    def highlightLayerInPreview(self, layer):
        for item in self.scene.items():
            if item.data(0) == layer.id:
                if hasattr(self.scene, 'currentEditableItem') and self.scene.currentEditableItem:
                    self.scene.currentEditableItem.removeBoundingBox()
                editable = self.scene.makeItemEditable(item)
                if editable:
                    editable.setupBoundingBox()
                    self.scene.currentEditableItem = editable
                break

    def highlightAnimationInPreview(self, layer, animation):
        self.animations = []
        
        item_to_animate = None
        for item in self.scene.items():
            if item.data(0) == layer.id:
                item_to_animate = item
                break
        
        if not item_to_animate:
            return
        
        if hasattr(animation, 'type'):
            if animation.type == "CAKeyframeAnimation":
                self.applyKeyframeAnimationToItem(item_to_animate, animation, layer)
            elif animation.type == "CASpringAnimation":
                self.applySpringAnimationToItem(item_to_animate, animation, layer)

        self.toggleAnimations()

    def previewState(self, layer, state_name):
        self.renderPreview(self.cafile.rootlayer, target_state=state_name)

    def applyStateToLayer(self, layer, item, target_state):
        if hasattr(layer, "states") and target_state in layer.states:
            state = layer.states[target_state]
            if hasattr(state, "elements"):
                for element in state.elements:
                    self.applyStateElementToItem(item, element, layer)

    def applyStateElementToItem(self, item, element, base_layer):
        target_layer = self.cafile.rootlayer.findlayer(element.targetId) if element.targetId != base_layer.id else base_layer
        target_item = self.findItemForLayer(target_layer)

        if target_item:
            if element.__class__.__name__ == "LKStateSetValue":
                setattr(target_layer, element.keyPath, element.value)
                self.applyStylesToItem(target_item, target_layer)
            elif element.__class__.__name__ == "LKStateAddAnimation":
                for anim in element.animations:
                    if anim.type == "CAKeyframeAnimation":
                        self.applyKeyframeAnimationToItem(target_item, anim, target_layer)
                    elif anim.type == "CASpringAnimation":
                        self.applySpringAnimationToItem(target_item, anim, target_layer)

    def findItemForLayer(self, layer):
        for item in self.scene.items():
            if item.data(0) == layer.id:
                return item
        return None

    def toggleAnimations(self):
        if not hasattr(self, 'animations') or not self.animations:
            return

        if self.animations_playing:
            for anim in self.animations:
                anim.pause()
            self.animations_playing = False
        else:
            for anim in self.animations:
                if anim.state() == QVariantAnimation.State.Paused:
                    anim.resume()
                else:
                    anim.start()
            self.animations_playing = True
        
        self.updateButtonIcons()

    def fitPreviewToView(self):
        if self.scene.items():
            self.ui.graphicsView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.ui.graphicsView.contentFittingZoom = self.ui.graphicsView.transform().m11()

    def zoomIn(self):
        self.ui.graphicsView.scale(1.1, 1.1)

    def zoomOut(self):
        self.ui.graphicsView.scale(1/1.1, 1/1.1)

    def keyPressEvent(self, event):
        mods = event.modifiers()
        if (mods & Qt.ControlModifier) or (self.isMacOS and (mods & Qt.MetaModifier)):
            if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
                self.zoomIn()
                return
            if event.key() in (Qt.Key_Minus, Qt.Key_Underscore):
                self.zoomOut()
                return
        super(PreviewRenderingMixin, self).keyPressEvent(event)