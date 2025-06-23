from PySide6.QtCore import Qt, QPointF, QRectF, Signal, QObject, QTimer, QEvent
from PySide6.QtGui import QColor, QPen, QBrush, QTransform, QCursor, QPainterPath, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsPathItem, QApplication, QStyleOptionGraphicsItem, QWidget
import math
import platform

class HandleType:
    TopLeft = 0
    Top = 1
    TopRight = 2
    Right = 3
    BottomRight = 4
    Bottom = 5
    BottomLeft = 6
    Left = 7
    Rotation = 8

class ResizeHandle(QGraphicsRectItem):
    """Visual handle for resizing operations"""
    def __init__(self, handle_type, parent=None):
        super().__init__(parent)
        self.handle_type = handle_type
        self.setRect(-4, -4, 8, 8)
        self.setBrush(QBrush(QColor(100, 150, 255)))
        self.setPen(QPen(QColor(50, 100, 200), 1))
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        
        cursor_map = {
            HandleType.TopLeft: Qt.SizeFDiagCursor,
            HandleType.Top: Qt.SizeVerCursor,
            HandleType.TopRight: Qt.SizeBDiagCursor,
            HandleType.Right: Qt.SizeHorCursor,
            HandleType.BottomRight: Qt.SizeFDiagCursor,
            HandleType.Bottom: Qt.SizeVerCursor,
            HandleType.BottomLeft: Qt.SizeBDiagCursor,
            HandleType.Left: Qt.SizeHorCursor,
            HandleType.Rotation: Qt.PointingHandCursor
        }
        self.setCursor(cursor_map.get(handle_type, Qt.ArrowCursor))

class EditableGraphicsItem(QObject):
    """A wrapper class that adds editing capabilities to QGraphicsItems"""
    itemChanged = Signal(QGraphicsItem)
    itemIsChanging = Signal(QGraphicsItem)
    transformChanged = Signal(QTransform)
    itemSelected = Signal(str)
    
    def __init__(self, item, parent=None):
        super(EditableGraphicsItem, self).__init__(parent)
        self.item = item
        self.handles = {}
        self.boundingRect = None
        self.rotationHandle = None
        self.boundingBoxItem = None
        self.isEditing = False
        self.originalTransform = QTransform(item.transform())
        self.initialClickPos = QPointF()
        self.initialItemPos = QPointF()
        self.initialItemTransform = QTransform()
        self.initialBoundingRect = QRectF()
        self.initialRotation = 0
        self.currentRotation = 0
        self.handleSize = 8
        self.rotateHandleSize = 10
        self.rotateHandleOffset = 20
        self.currentHandle = None
        self.aspectRatioLocked = False
        
        self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.item.setAcceptHoverEvents(True)
    
    def setupBoundingBox(self):
        """Create bounding box and handles for the item"""
        if not self.item.scene():
            return
            
        self.removeBoundingBox()
            
        scene = self.item.scene()
        rect = self.item.boundingRect()
        
        self.boundingBoxItem = QGraphicsRectItem(rect)
        self.boundingBoxItem.setPen(QPen(QColor(100, 150, 255), 1, Qt.DashLine))
        self.boundingBoxItem.setBrush(QBrush(Qt.transparent))
        self.boundingBoxItem.setParentItem(self.item)
        self.boundingBoxItem.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)
        
        handle_positions = [
            (rect.topLeft(), HandleType.TopLeft),
            (QPointF(rect.center().x(), rect.top()), HandleType.Top),
            (rect.topRight(), HandleType.TopRight),
            (QPointF(rect.right(), rect.center().y()), HandleType.Right),
            (rect.bottomRight(), HandleType.BottomRight),
            (QPointF(rect.center().x(), rect.bottom()), HandleType.Bottom),
            (rect.bottomLeft(), HandleType.BottomLeft),
            (QPointF(rect.left(), rect.center().y()), HandleType.Left),
        ]
        
        for pos, handle_type in handle_positions:
            handle = ResizeHandle(handle_type)
            handle.setPos(pos)
            handle.setParentItem(self.item)
            handle.setFlag(QGraphicsItem.ItemIgnoresParentOpacity, True)
            self.handles[handle_type] = handle
        
        rotation_pos = QPointF(rect.center().x(), rect.top() - self.rotateHandleOffset)
        self.rotationHandle = ResizeHandle(HandleType.Rotation)
        self.rotationHandle.setPos(rotation_pos)
        self.rotationHandle.setParentItem(self.item)
        self.rotationHandle.setBrush(QBrush(QColor(255, 100, 100)))
        self.rotationHandle.setPen(QPen(QColor(200, 50, 50), 1))
        self.rotationHandle.setFlag(QGraphicsItem.ItemIgnoresParentOpacity, True)
    
    def removeBoundingBox(self):
        """Remove bounding box and handles"""
        try:
            if self.boundingBoxItem and not self.isItemDeleted(self.boundingBoxItem):
                scene = self.boundingBoxItem.scene()
                if scene:
                    scene.removeItem(self.boundingBoxItem)
                self.boundingBoxItem = None
        except (RuntimeError, AttributeError):
            self.boundingBoxItem = None
        
        handles_to_remove = list(self.handles.values())
        for handle in handles_to_remove:
            try:
                if not self.isItemDeleted(handle):
                    scene = handle.scene()
                    if scene:
                        scene.removeItem(handle)
            except (RuntimeError, AttributeError):
                pass
        self.handles.clear()
        
        try:
            if self.rotationHandle and not self.isItemDeleted(self.rotationHandle):
                scene = self.rotationHandle.scene()
                if scene:
                    scene.removeItem(self.rotationHandle)
                self.rotationHandle = None
        except (RuntimeError, AttributeError):
            self.rotationHandle = None

    def isItemDeleted(self, item):
        """Check if a QGraphicsItem has been deleted by Qt"""
        try:
            _ = item.pos()
            return False
        except (RuntimeError, AttributeError):
            return True
    
    def updateBoundingBox(self):
        """Update the position of bounding box and handles after item moves"""
        try:
            if self.isItemDeleted(self.item):
                if self.boundingBoxItem or self.handles or self.rotationHandle:
                    print(f"Main item {id(self.item)} deleted. Removing its bounding box and handles.")
                self.removeBoundingBox()
                return

            if not self.boundingBoxItem or self.isItemDeleted(self.boundingBoxItem):
                if self.boundingBoxItem and self.isItemDeleted(self.boundingBoxItem):
                    self.boundingBoxItem = None
                return 

            rect = self.item.boundingRect()
            self.boundingBoxItem.setRect(rect)
            
            handle_positions = {
                HandleType.TopLeft: rect.topLeft(),
                HandleType.Top: QPointF(rect.center().x(), rect.top()),
                HandleType.TopRight: rect.topRight(),
                HandleType.Right: QPointF(rect.right(), rect.center().y()),
                HandleType.BottomRight: rect.bottomRight(),
                HandleType.Bottom: QPointF(rect.center().x(), rect.bottom()),
                HandleType.BottomLeft: rect.bottomLeft(),
                HandleType.Left: QPointF(rect.left(), rect.center().y()),
            }
            
            active_handle_types = list(self.handles.keys())
            for handle_type in active_handle_types:
                handle = self.handles.get(handle_type)
                if handle:
                    if not self.isItemDeleted(handle):
                        handle.setPos(handle_positions[handle_type])
                    else:
                        del self.handles[handle_type]
            
            if self.rotationHandle:
                if not self.isItemDeleted(self.rotationHandle):
                    rotation_pos = QPointF(rect.center().x(), rect.top() - self.rotateHandleOffset)
                    self.rotationHandle.setPos(rotation_pos)
                else:
                    self.rotationHandle = None
                
        except (RuntimeError, AttributeError) as e:
            print(f"Error during updateBoundingBox for item {id(self.item if self.item else 'None')}: {e}")
            if self.item and self.isItemDeleted(self.item):
                print(f"Main item {id(self.item)} confirmed deleted after error. Removing bounding box.")
                self.removeBoundingBox()
            else:
                print(f"Error in updateBoundingBox, but main item not detected as deleted or item is None. Bounding box NOT removed solely due to this error.")
    
    def startEdit(self, handle_type, handle_pos):
        """Start edit operation (resize or rotate)"""
        self.isEditing = True
        self.currentHandle = handle_type
        self.initialClickPos = handle_pos
        self.initialItemPos = self.item.pos()
        self.initialItemTransform = QTransform(self.item.transform())
        self.initialBoundingRect = self.item.boundingRect()
        
        if handle_type == HandleType.Rotation:
            self.initialRotation = self.getItemRotation()
            center = self.item.mapToScene(self.initialBoundingRect.center())
            dx = handle_pos.x() - center.x()
            dy = handle_pos.y() - center.y()
            self.initialAngle = math.degrees(math.atan2(dy, dx))
        
        if hasattr(self.item, 'rect'):
            self.originalRect = self.item.rect()
        else:
            self.originalRect = self.item.boundingRect()
        
        if hasattr(self.item, 'path'):
            self.original_path_at_drag_start = self.item.path()
    
    def handleEditOperation(self, new_pos):
        """Handle move, resize, or rotate operations"""
        if not self.isEditing or self.currentHandle is None:
            return
            
        if self.currentHandle == HandleType.Rotation:
            self.handleRotation(new_pos)
        else:
            self.handleResize(new_pos)
        
        self.updateBoundingBox()
        self.itemIsChanging.emit(self.item)
    
    def handleRotation(self, mouse_pos):
        """Handle rotation operation"""
        center = self.item.mapToScene(self.initialBoundingRect.center())
        
        dx = mouse_pos.x() - center.x()
        dy = mouse_pos.y() - center.y()
        current_angle = math.degrees(math.atan2(dy, dx))
        
        rotation_delta = current_angle - self.initialAngle
        
        transform = QTransform()
        transform.translate(self.initialItemPos.x(), self.initialItemPos.y())
        transform.rotate(self.initialRotation + rotation_delta)
        transform.translate(-self.initialItemPos.x(), -self.initialItemPos.y())
        
        self.item.setTransform(self.initialItemTransform * transform)
        
    def handleResize(self, mouse_pos_scene):
        handle_type = self.currentHandle
        
        inverted_transform, _ = self.initialItemTransform.inverted()
        mouse_pos_item = inverted_transform.map(mouse_pos_scene)
        
        initial_pos_item = inverted_transform.map(self.initialClickPos)
        
        delta = mouse_pos_item - initial_pos_item
        
        new_rect = QRectF(self.initialBoundingRect)
        
        if handle_type == HandleType.TopLeft:
            new_rect.setTopLeft(new_rect.topLeft() + delta)
        elif handle_type == HandleType.Top:
            new_rect.setTop(new_rect.top() + delta.y())
        elif handle_type == HandleType.TopRight:
            new_rect.setTopRight(new_rect.topRight() + delta)
        elif handle_type == HandleType.Right:
            new_rect.setRight(new_rect.right() + delta.x())
        elif handle_type == HandleType.BottomRight:
            new_rect.setBottomRight(new_rect.bottomRight() + delta)
        elif handle_type == HandleType.Bottom:
            new_rect.setBottom(new_rect.bottom() + delta.y())
        elif handle_type == HandleType.BottomLeft:
            new_rect.setBottomLeft(new_rect.bottomLeft() + delta)
        elif handle_type == HandleType.Left:
            new_rect.setLeft(new_rect.left() + delta.x())
        
        # To prevent inverted rects
        if new_rect.width() < 1: new_rect.setWidth(1)
        if new_rect.height() < 1: new_rect.setHeight(1)

        # This part requires the item to have a setRect or similar method.
        # This will work for QGraphicsRectItem, but for QGraphicsPixmapItem etc.,
        # we need to adjust scale, not rect.
        
        # For now, let's assume we can scale based on rect change
        x_scale = new_rect.width() / self.initialBoundingRect.width() if self.initialBoundingRect.width() != 0 else 1
        y_scale = new_rect.height() / self.initialBoundingRect.height() if self.initialBoundingRect.height() != 0 else 1
        
        new_transform = QTransform(self.initialItemTransform)
        
        # We need to translate to origin, scale, and translate back
        center = self.initialBoundingRect.center()
        new_transform.translate(center.x(), center.y())
        new_transform.scale(x_scale, y_scale)
        new_transform.translate(-center.x(), -center.y())
        
        self.item.setTransform(new_transform)

    def endEdit(self):
        """End edit operation"""
        if self.isEditing:
            self.itemChanged.emit(self.item)
        self.isEditing = False
        self.currentHandle = None

    def getItemRotation(self):
        """Get the item's rotation from its transform"""
        return self.item.rotation()

class CheckerboardGraphicsScene(QGraphicsScene):
    itemSelectedOnCanvas = Signal(str)
    
    def __init__(self, parent=None):
        super(CheckerboardGraphicsScene, self).__init__(parent)
        self.color1 = QColor(220, 220, 220)
        self.color2 = QColor(240, 240, 240)
        self.tileSize = 20
        self.editMode = False
        self.editableItems = {}
        self.currentEditableItem = None
        self.dragInProgress = False
        self.lastMousePos = QPointF()

    def setBackgroundColor(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.update()

    def drawBackground(self, painter, rect):
        painter.save()
        painter.setPen(Qt.NoPen)
        
        for y in range(int(rect.top()), int(rect.bottom()), self.tileSize):
            for x in range(int(rect.left()), int(rect.right()), self.tileSize):
                if (x // self.tileSize + y // self.tileSize) % 2 == 0:
                    painter.setBrush(self.color1)
                else:
                    painter.setBrush(self.color2)
                painter.drawRect(x, y, self.tileSize, self.tileSize)
        
        painter.restore()

    def setEditMode(self, enabled):
        self.editMode = enabled
        if not enabled:
            self.deselectAllItems()
            for item in self.items():
                item.setFlag(QGraphicsItem.ItemIsMovable, False)
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
        else:
            for item in self.items():
                if item.data(1) == "Layer":
                    item.setFlag(QGraphicsItem.ItemIsMovable, True)
                    item.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def makeItemEditable(self, item):
        if self.isItemDeleted(item):
            return None
        item_id = id(item)
        if item_id not in self.editableItems:
            editable = EditableGraphicsItem(item)
            self.editableItems[item_id] = editable
        return self.editableItems[item_id]

    def mousePressEvent(self, event):
        if not self.editMode:
            super(CheckerboardGraphicsScene, self).mousePressEvent(event)
            return
            
        pos = event.scenePos()
        items_at_pos = self.items(pos)
        
        # Check if a handle was clicked first
        for item in items_at_pos:
            if isinstance(item, ResizeHandle):
                # Look up the EditableGraphicsItem wrapper for the handle's parent
                editable_parent = self.editableItems.get(id(item.parentItem()))
                if editable_parent:
                    self.currentEditableItem = editable_parent
                    self.dragInProgress = True
                    # Correctly start the edit operation on the wrapper
                    self.currentEditableItem.startEdit(item.handle_type, pos)
                    event.accept()
                    return

        # If not a handle, proceed with normal selection/move
        top_item = self.itemAt(pos, QTransform())
        if top_item and top_item.data(1) == "Layer":
            self.selectItem(top_item)
            self.dragInProgress = False
        else:
            self.deselectAllItems()
        
        super(CheckerboardGraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.editMode and self.currentEditableItem and self.dragInProgress:
            self.currentEditableItem.handleEditOperation(event.scenePos())
            event.accept()
            return
        super(CheckerboardGraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.editMode and self.currentEditableItem:
            if self.dragInProgress:
                 self.currentEditableItem.endEdit()
            # After finishing an edit or move, ensure the bounding box is up to date
            self.currentEditableItem.updateBoundingBox()
            
        self.dragInProgress = False
        super(CheckerboardGraphicsScene, self).mouseReleaseEvent(event)

    def selectItem(self, item):
        if self.isItemDeleted(item):
            self.currentEditableItem = None
            return
            
        self.deselectAllItems(item_to_keep=item)
        
        editable = self.makeItemEditable(item)
        if editable:
            self.currentEditableItem = editable
            editable.setupBoundingBox()
            self.itemSelectedOnCanvas.emit(item.data(0))
        
        item.setSelected(True)

    def deselectAllItems(self, item_to_keep=None):
        if self.currentEditableItem and (not item_to_keep or self.currentEditableItem.item != item_to_keep):
            self.currentEditableItem.removeBoundingBox()
            self.currentEditableItem = None
            
        for item in self.items():
            if item != item_to_keep:
                item.setSelected(False)

    def isItemDeleted(self, item):
        try:
            _ = item.pos()
            return False
        except RuntimeError:
            return True

    def onItemChanged(self, item):
        editable = self.editableItems.get(id(item))
        if editable:
            editable.updateBoundingBox()

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None, min_zoom=0.05, max_zoom=10.0):
        super(CustomGraphicsView, self).__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setInteractive(True)
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        
        self.isMacOS = platform.system() == "Darwin"
        if self.isMacOS:
            self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.viewport().setAttribute(Qt.WA_AcceptTouchEvents, True)
            self.grabGesture(Qt.PinchGesture)

    def setEditMode(self, enabled):
        if enabled:
            self.setDragMode(QGraphicsView.NoDrag)
            if hasattr(self.scene(), 'setEditMode'):
                self.scene().setEditMode(True)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            if hasattr(self.scene(), 'setEditMode'):
                self.scene().setEditMode(False)

    def wheelEvent(self, event):
        if self.isMacOS and (event.modifiers() == Qt.NoModifier or event.modifiers() == Qt.ShiftModifier):
            # Scrolling gesture on macOS
            delta = event.angleDelta()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        elif event.modifiers() & Qt.ControlModifier or (self.isMacOS and event.modifiers() & Qt.MetaModifier):
            # Zooming
            delta = event.angleDelta().y()
            self.handleZoom(delta)
            event.accept()
        else:
            super(CustomGraphicsView, self).wheelEvent(event)

    def handleZoom(self, delta):
        zoom_factor = 1.15 if delta > 0 else 1 / 1.15
        
        current_transform = self.transform()
        
        if (delta > 0 and current_transform.m11() * zoom_factor > self.max_zoom) or \
           (delta < 0 and current_transform.m11() * zoom_factor < self.min_zoom):
            return
            
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.viewport().setCursor(Qt.ClosedHandCursor)
        super(CustomGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(CustomGraphicsView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.viewport().setCursor(Qt.OpenHandCursor)
        super(CustomGraphicsView, self).mouseReleaseEvent(event)

    def event(self, event):
        if self.isMacOS and event.type() == QEvent.Gesture:
            return self.handleGestureEvent(event.gesture(Qt.PinchGesture))
        return super(CustomGraphicsView, self).event(event)

    def handleGestureEvent(self, gesture):
        if gesture:
            if gesture.state() == Qt.GestureStarted:
                self.gesture_started_transform = self.transform()
            
            if gesture.state() == Qt.GestureUpdated:
                scale_factor = gesture.scaleFactor()
                
                # Prevent extreme zooming
                if (self.gesture_started_transform.m11() * scale_factor > self.max_zoom) or \
                   (self.gesture_started_transform.m11() * scale_factor < self.min_zoom):
                    return True
                
                # Apply zoom
                new_transform = QTransform(self.gesture_started_transform)
                
                # Get the center point of the gesture in scene coordinates
                center_point = self.mapToScene(gesture.hotSpot().toPoint())
                
                new_transform.translate(center_point.x(), center_point.y())
                new_transform.scale(scale_factor, scale_factor)
                new_transform.translate(-center_point.x(), -center_point.y())
                
                self.setTransform(new_transform)

            return True
        return False

    def updateContentFittingZoom(self, sceneRect):
        if sceneRect.isEmpty():
            return
        
        viewRect = self.viewport().rect()
        
        if viewRect.width() <= 0 or viewRect.height() <= 0:
            return
            
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        
        self.contentFittingZoom = min(x_ratio, y_ratio) * 0.95

def create_sample_scene():
    scene = CheckerboardGraphicsScene()
    
    rect_item = QGraphicsRectItem(0, 0, 100, 50)
    rect_item.setBrush(QColor(255, 0, 0, 150))
    rect_item.setPen(Qt.NoPen)
    rect_item.setPos(50, 50)
    rect_item.setData(0, "rect1")
    rect_item.setData(1, "Layer")
    scene.addItem(rect_item)
    
    ellipse_item = QGraphicsEllipseItem(0, 0, 80, 80)
    ellipse_item.setBrush(QColor(0, 0, 255, 150))
    ellipse_item.setPen(Qt.NoPen)
    ellipse_item.setPos(200, 80)
    ellipse_item.setData(0, "ellipse1")
    ellipse_item.setData(1, "Layer")
    scene.addItem(ellipse_item)
    
    scene.setEditMode(True)
    
    return scene