import re
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QMessageBox, QTreeWidgetItemIterator
from PySide6.QtGui import QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QSize

class InspectorManagementMixin:
    def populateLayersTreeWidget(self):
        if hasattr(self, 'cafile') and self.cafile and self.cafile.rootlayer:
            rootItem = QTreeWidgetItem([self.cafile.rootlayer.name, "Root", self.cafile.rootlayer.id, ""])
            rootItem.setSizeHint(0, QSize(0, 40))
            self.ui.treeWidget.addTopLevelItem(rootItem)
            if len(self.cafile.rootlayer._sublayerorder) > 0:
                self.treeWidgetChildren(rootItem, self.cafile.rootlayer)

        self.ui.addButton.setEnabled(self.isDirty)

    def treeWidgetChildren(self, item: QTreeWidgetItem, layer) -> None:
        for id in getattr(layer, '_sublayerorder', []):
            sublayer = getattr(layer, 'sublayers', {}).get(id)
            if sublayer is None:
                continue
            childItem = QTreeWidgetItem([getattr(sublayer, 'name', ''), "Layer", getattr(sublayer, 'id', ''), getattr(layer, 'id', '')])
            childItem.setSizeHint(0, QSize(0, 40))
            
            if hasattr(self, 'missing_assets') and hasattr(sublayer, '_content') and sublayer._content is not None:
                if hasattr(sublayer, "content") and hasattr(sublayer.content, 'src'):
                    if sublayer.content.src in self.missing_assets:
                        childItem.setText(0, "⚠️ " + getattr(sublayer, 'name', ''))
                        childItem.setForeground(0, QColor(255, 0, 0))
            
            item.addChild(childItem)

            if hasattr(sublayer, '_sublayerorder') and len(sublayer._sublayerorder) > 0:
                self.treeWidgetChildren(childItem, sublayer)
            if hasattr(sublayer, '_animations') and sublayer._animations is not None:
                for animation in getattr(sublayer, 'animations', []):
                    animItem = QTreeWidgetItem([getattr(animation, 'keyPath', ''), "Animation", "", getattr(sublayer, 'id', '')])
                    animItem.setSizeHint(0, QSize(0, 40))
                    childItem.addChild(animItem)
                    
    def openInInspector(self, current: QTreeWidgetItem, _) -> None:
        if current is None:
            if hasattr(self.scene, 'currentEditableItem') and self.scene.currentEditableItem:
                self.scene.currentEditableItem.removeBoundingBox()
                self.scene.currentEditableItem = None
            self.ui.tableWidget.blockSignals(True)
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.blockSignals(False)
            self.currentInspectObject = None
            return
        self.ui.tableWidget.blockSignals(True)
        self.currentInspectObject = None

        if hasattr(self.scene, 'currentEditableItem') and self.scene.currentEditableItem:
            self.scene.currentEditableItem.removeBoundingBox()
            self.scene.currentEditableItem = None

        self.currentSelectedItem = current
        self.ui.tableWidget.setRowCount(0)
        row_index = 0

        element_type = current.text(1)
        if element_type == "Animation":
            parent = self.cafile.rootlayer.findlayer(current.text(3))
            element = parent.findanimation(current.text(0)) if parent is not None else None
            if element:
                self.currentInspectObject = element
                row_index = self.add_category_header("Basic Info", row_index)
                self.add_inspector_row("NAME", current.text(0), row_index)
                row_index += 1
                self.add_inspector_row("TYPE", element.type, row_index)
                row_index += 1

                # Timing properties
                if (
                    (hasattr(element, "duration") and element.duration)
                    or (hasattr(element, "beginTime") and element.beginTime)
                    or (hasattr(element, "fillMode") and element.fillMode)
                    or (hasattr(element, "removedOnCompletion") and element.removedOnCompletion)
                    or (hasattr(element, "repeatCount") and element.repeatCount)
                    or (hasattr(element, "calculationMode") and element.calculationMode)
                ):
                    row_index = self.add_category_header("Timing", row_index)
                
                if hasattr(element, "duration") and element.duration:
                    self.add_inspector_row("DURATION", self.formatFloat(element.duration), row_index)
                    row_index += 1
                
                if hasattr(element, "beginTime") and element.beginTime:
                    self.add_inspector_row("BEGIN TIME", self.formatFloat(element.beginTime), row_index)
                    row_index += 1
                if hasattr(element, "duration") and element.duration:
                    self.add_inspector_row("DURATION", self.formatFloat(element.duration), row_index)
                    row_index += 1

                if hasattr(element, "beginTime") and element.beginTime:
                    self.add_inspector_row("BEGIN TIME", self.formatFloat(element.beginTime), row_index)
                    row_index += 1

                if hasattr(element, "fillMode") and element.fillMode:
                    self.add_inspector_row("FILL MODE", element.fillMode, row_index)
                    row_index += 1

                if hasattr(element, "removedOnCompletion") and element.removedOnCompletion:
                    self.add_inspector_row("REMOVED ON COMPLETION", element.removedOnCompletion, row_index)
                    row_index += 1

                if hasattr(element, "repeatCount") and element.repeatCount:
                    self.add_inspector_row("REPEAT COUNT", self.formatFloat(element.repeatCount), row_index)
                    row_index += 1

                if hasattr(element, "calculationMode") and element.calculationMode:
                    self.add_inspector_row("CALCULATION MODE", element.calculationMode, row_index)
                    row_index += 1

                # Spring Animation properties
                if getattr(element, "type", "") == "CASpringAnimation":
                    row_index = self.add_category_header("Spring Properties", row_index)
                    if hasattr(element, "damping") and element.damping:
                        self.add_inspector_row("DAMPING", self.formatFloat(element.damping), row_index)
                        row_index += 1
                    if hasattr(element, "mass") and element.mass:
                        self.add_inspector_row("MASS", self.formatFloat(element.mass), row_index)
                        row_index += 1
                    if hasattr(element, "stiffness") and element.stiffness:
                        self.add_inspector_row("STIFFNESS", self.formatFloat(element.stiffness), row_index)
                        row_index += 1
                    if hasattr(element, "velocity") and element.velocity:
                        self.add_inspector_row("VELOCITY", self.formatFloat(element.velocity), row_index)
                        row_index += 1
                    if hasattr(element, "mica_autorecalculatesDuration"):
                        self.add_inspector_row("AUTO RECALCULATES DURATION", element.mica_autorecalculatesDuration, row_index)
                        row_index += 1

                # Keyframe Animation properties
                if getattr(element, "type", "") == "CAKeyframeAnimation":
                    row_index = self.add_category_header("Keyframe Data", row_index)
                    if hasattr(element, "values") and element.values:
                        values_str = ", ".join([str(self.formatFloat(value.value)) for value in element.values])
                        self.add_inspector_row("VALUES", values_str, row_index)
                        row_index += 1
                    if hasattr(element, "keyTimes") and element.keyTimes:
                        times_str = ", ".join([str(self.formatFloat(time.value)) for time in element.keyTimes])
                        self.add_inspector_row("KEY TIMES", times_str, row_index)
                        row_index += 1
                    if hasattr(element, "timingFunctions") and element.timingFunctions:
                        self.add_inspector_row("TIMING FUNCTIONS", str(len(element.timingFunctions)), row_index)
                        row_index += 1
                    if hasattr(element, "path") and element.path:
                        self.add_inspector_row("PATH", "Path Animation", row_index)
                        row_index += 1

                # Match Move Animation properties
                if getattr(element, "type", "") == "CAMatchMoveAnimation":
                    row_index = self.add_category_header("Match Move Properties", row_index)
                    if hasattr(element, "additive") and element.additive:
                        self.add_inspector_row("ADDITIVE", element.additive, row_index)
                        row_index += 1
                    if hasattr(element, "appliesX") and element.appliesX:
                        self.add_inspector_row("APPLIES X", element.appliesX, row_index)
                        row_index += 1
                    if hasattr(element, "appliesY") and element.appliesY:
                        self.add_inspector_row("APPLIES Y", element.appliesY, row_index)
                        row_index += 1
                    if hasattr(element, "appliesScale") and element.appliesScale:
                        self.add_inspector_row("APPLIES SCALE", element.appliesScale, row_index)
                        row_index += 1
                    if hasattr(element, "appliesRotation") and element.appliesRotation:
                        self.add_inspector_row("APPLIES ROTATION", element.appliesRotation, row_index)
                        row_index += 1
                
                self.highlightAnimationInPreview(parent, element)
                
        elif element_type == "Layer" or element_type == "Root":
            if element_type == "Layer":
                element = self.cafile.rootlayer.findlayer(current.text(2))
            else:
                element = self.cafile.rootlayer
                
            if element:
                self.currentInspectObject = element

                if hasattr(self, 'scene') and self.scene:
                    for item_in_scene in self.scene.items():
                        if hasattr(item_in_scene, 'data') and item_in_scene.data(0) == element.id and item_in_scene.data(1) == "Layer":
                            editable_item = self.scene.makeItemEditable(item_in_scene)
                            if editable_item:
                                if hasattr(self.scene, 'currentEditableItem') and self.scene.currentEditableItem and self.scene.currentEditableItem != editable_item:
                                    self.scene.currentEditableItem.removeBoundingBox()
                                editable_item.setupBoundingBox()
                                self.scene.currentEditableItem = editable_item
                            break

                row_index = self.add_category_header("Basic Info", row_index)
                
                self.add_inspector_row("NAME", current.text(0), row_index)
                row_index += 1
                
                self.add_inspector_row("ID", element.id, row_index)
                row_index += 1
                
                layer_type = "CALayer"
                if hasattr(element, "layer_class") and element.layer_class:
                    layer_type = element.layer_class
                
                self.add_inspector_row("CLASS", layer_type, row_index)
                row_index += 1

                row_index = self.add_category_header("Geometry", row_index)

                if hasattr(element, "bounds"):
                    self.add_inspector_row("BOUNDS", self.formatPoint(element.bounds), row_index)
                    row_index += 1
                
                if hasattr(element, "position"):
                    self.add_inspector_row("POSITION", self.formatPoint(element.position), row_index)
                    row_index += 1

                if hasattr(element, "zPosition"):
                    self.add_inspector_row("Z POSITION", self.formatFloat(element.zPosition), row_index)
                    row_index += 1

                if hasattr(element, "anchorPoint"):
                    self.add_inspector_row("ANCHOR POINT", self.formatPoint(element.anchorPoint), row_index)
                    row_index += 1

                if hasattr(element, "transform"):
                    transform_str = self.parseTransform(element.transform)
                    self.add_inspector_row("TRANSFORM", transform_str, row_index)
                    row_index += 1

                row_index = self.add_category_header("Appearance", row_index)

                if hasattr(element, "opacity"):
                    self.add_inspector_row("OPACITY", self.formatFloat(element.opacity), row_index)
                    row_index += 1

                if hasattr(element, "hidden"):
                    self.add_inspector_row("HIDDEN", str(element.hidden), row_index)
                    row_index += 1

                if hasattr(element, "masksToBounds"):
                    self.add_inspector_row("MASKS TO BOUNDS", str(element.masksToBounds), row_index)
                    row_index += 1
                    
                if hasattr(element, "doubleSided"):
                    self.add_inspector_row("DOUBLE SIDED", str(element.doubleSided), row_index)
                    row_index += 1
                
                if hasattr(element, "geometryFlipped"):
                    self.add_inspector_row("GEOMETRY FLIPPED", str(element.geometryFlipped), row_index)
                    row_index += 1

                row_index = self.add_category_header("Border", row_index)
                if hasattr(element, "borderWidth"):
                    self.add_inspector_row("BORDER WIDTH", self.formatFloat(element.borderWidth), row_index)
                    row_index += 1
                if hasattr(element, "borderColor"):
                    color = self.parseColor(element.borderColor)
                    self.add_inspector_row("BORDER COLOR", color, row_index)
                    row_index += 1

                row_index = self.add_category_header("Shadow", row_index)
                if hasattr(element, "shadowColor"):
                    color = self.parseColor(element.shadowColor)
                    self.add_inspector_row("SHADOW COLOR", color, row_index)
                    row_index += 1

                if hasattr(element, "shadowOpacity"):
                    self.add_inspector_row("SHADOW OPACITY", self.formatFloat(element.shadowOpacity), row_index)
                    row_index += 1

                if hasattr(element, "shadowOffset"):
                    self.add_inspector_row("SHADOW OFFSET", self.formatPoint(element.shadowOffset), row_index)
                    row_index += 1

                if hasattr(element, "shadowRadius"):
                    self.add_inspector_row("SHADOW RADIUS", self.formatFloat(element.shadowRadius), row_index)
                    row_index += 1

                if hasattr(element, "shadowPath"):
                    self.add_inspector_row("SHADOW PATH", str(element.shadowPath), row_index)
                    row_index += 1
                
                # Contents
                if hasattr(element, "contents"):
                    row_index = self.add_category_header("Contents", row_index)
                    if hasattr(element, "contents") and isinstance(element.contents, dict):
                        for key, val in element.contents.items():
                            self.add_inspector_row(key.upper(), str(val), row_index)
                            row_index += 1
                    else:
                        self.add_inspector_row("CONTENTS", str(element.contents), row_index)
                        row_index += 1

                # Text Layer properties
                if layer_type == "CATextLayer":
                    row_index = self.add_category_header("Text Properties", row_index)
                    if hasattr(element, "string"):
                        self.add_inspector_row("STRING", str(element.string), row_index)
                        row_index += 1
                    if hasattr(element, "font"):
                        self.add_inspector_row("FONT", str(element.font), row_index)
                        row_index += 1
                    if hasattr(element, "fontSize"):
                        self.add_inspector_row("FONT SIZE", self.formatFloat(element.fontSize), row_index)
                        row_index += 1
                    if hasattr(element, "foregroundColor"):
                        color = self.parseColor(element.foregroundColor)
                        self.add_inspector_row("FOREGROUND COLOR", color, row_index)
                        row_index += 1
                    if hasattr(element, "alignmentMode"):
                        self.add_inspector_row("ALIGNMENT MODE", str(element.alignmentMode), row_index)
                        row_index += 1
                    if hasattr(element, "truncationMode"):
                        self.add_inspector_row("TRUNCATION MODE", str(element.truncationMode), row_index)
                        row_index += 1
                    if hasattr(element, "wrapped"):
                        self.add_inspector_row("WRAPPED", str(element.wrapped), row_index)
                        row_index += 1
                        
                # Custom Properties
                if hasattr(element, 'custom_properties'):
                    row_index = self.add_category_header("Custom Properties", row_index)
                    for key, val in element.custom_properties.items():
                        self.add_inspector_row(key, str(val), row_index)
                        row_index += 1

        self.ui.tableWidget.blockSignals(False)

    def add_category_header(self, category_name, row_index):
        self.ui.tableWidget.insertRow(row_index)
        header_item = QTableWidgetItem(category_name)
        header_item.setFlags(Qt.NoItemFlags)
        
        if self.isDarkMode:
            header_item.setBackground(QColor(60, 60, 60))
            header_item.setForeground(QColor(230, 230, 230))
        else:
            header_item.setBackground(QColor(220, 220, 220))
            header_item.setForeground(QColor(30, 30, 30))
            
        font = QFont()
        font.setBold(True)
        header_item.setFont(font)
        
        self.ui.tableWidget.setSpan(row_index, 0, 1, 2)
        self.ui.tableWidget.setItem(row_index, 0, header_item)
        return row_index + 1

    def add_inspector_row(self, key, value, row_index):
        self.ui.tableWidget.insertRow(row_index)
        key_item = QTableWidgetItem(key)
        key_item.setFlags(Qt.ItemIsEnabled)
        
        value_item = None
        
        if key == "ID" or "CLASS" in key:
            value_item = QTableWidgetItem(str(value))
            value_item.setFlags(Qt.ItemIsEnabled)
        elif key == "BORDER COLOR" or key == "SHADOW COLOR" or key == "FOREGROUND COLOR" or key == "BACKGROUND COLOR":
            value_item = QTableWidgetItem(str(value))
            
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(value) if isinstance(value, str) and "#" in value else Qt.transparent)
            value_item.setIcon(QIcon(pixmap))
        else:
            value_item = QTableWidgetItem(str(value))
            value_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)

        if self.isDarkMode:
            key_item.setForeground(QColor(200, 200, 200))
            if value_item:
                value_item.setForeground(QColor(200, 200, 200))
        else:
            key_item.setForeground(QColor(50, 50, 50))
            if value_item:
                value_item.setForeground(QColor(50, 50, 50))

        self.ui.tableWidget.setItem(row_index, 0, key_item)
        if value_item:
            self.ui.tableWidget.setItem(row_index, 1, value_item)

    def populateStatesTreeWidget(self):
        if hasattr(self, 'cafile') and self.cafile:
            self.ui.statesTreeWidget.clear()
            self.processStatesInLayer(self.cafile.rootlayer, None)
    
    def processStatesInLayer(self, layer, parentItem):
        if hasattr(layer, 'states') and layer.states:
            layerItem = QTreeWidgetItem([layer.name, "Layer", layer.id])
            layerItem.setSizeHint(0, QSize(0, 40))
            
            if parentItem:
                parentItem.addChild(layerItem)
            else:
                self.ui.statesTreeWidget.addTopLevelItem(layerItem)

            self.addStateElements(layer, layerItem)
        
        if hasattr(layer, 'sublayers') and hasattr(layer, '_sublayerorder'):
            for sub_id in layer._sublayerorder:
                sublayer = layer.sublayers.get(sub_id)
                if sublayer:
                    self.processStatesInLayer(sublayer, layerItem if 'layerItem' in locals() else parentItem)

    def addStateElements(self, state, stateItem):
        if hasattr(state, "elements") and state.elements:
            for element in state.elements:
                if element.__class__.__name__ == "LKStateSetValue":
                    setItem = QTreeWidgetItem([element.keyPath, "SetValue", element.targetId])
                    setItem.setSizeHint(0, QSize(0, 40))
                    stateItem.addChild(setItem)
                elif element.__class__.__name__ == "LKStateAddAnimation":
                    animItem = QTreeWidgetItem([element.keyPath, "AddAnimation", element.targetId])
                    animItem.setSizeHint(0, QSize(0, 40))
                    stateItem.addChild(animItem)
        
        if hasattr(state, "transitions") and state.transitions:
            for key, transition in state.transitions.items():
                transItem = QTreeWidgetItem([key, "Transition", transition.targetId])
                transItem.setSizeHint(0, QSize(0, 40))
                stateItem.addChild(transItem)

    def openStateInInspector(self, current, _):
        if not current:
            self.ui.tableWidget.setRowCount(0)
            return
            
        self.ui.tableWidget.setRowCount(0)
        row_index = 0
        
        item_type = current.text(1)
        
        if item_type == "State":
            row_index = self._handle_state(current, row_index)
        elif item_type == "Transition":
            row_index = self._handle_transition(current, row_index)
        elif item_type == "SetValue":
            row_index = self._handle_set_value(current, row_index)
        elif item_type == "AddAnimation":
            row_index = self._handle_add_animation(current, row_index)
        elif item_type == "TransitionElement":
            row_index = self._handle_transition_element(current, row_index)
            
    def _handle_state(self, current, row_index):
        row_index = self.add_category_header("State Details", row_index)
        
        state_name = current.text(0)
        self.add_inspector_row("STATE NAME", state_name, row_index)
        row_index += 1
        
        layer_id = current.text(2)
        if layer_id:
            self.add_inspector_row("LAYER ID", layer_id, row_index)
            row_index += 1
            layer = self.cafile.rootlayer.findlayer(layer_id)
            if layer and hasattr(layer, "name"):
                self.add_inspector_row("LAYER NAME", layer.name, row_index)
                row_index += 1
        else:
             self.add_inspector_row("LAYER", "Root Layer", row_index)
             row_index += 1

        layer = self.cafile.rootlayer.findlayer(layer_id) if layer_id else self.cafile.rootlayer
        if layer and hasattr(layer, 'states') and state_name in layer.states:
            state = layer.states[state_name]
            
            if hasattr(state, 'basedOn') and state.basedOn:
                self.add_inspector_row("BASED ON", state.basedOn, row_index)
                row_index += 1
            
            if hasattr(state, 'elements') and state.elements:
                self.add_inspector_row("ELEMENT COUNT", str(len(state.elements)), row_index)
                row_index += 1
            
            if hasattr(state, 'transitions') and state.transitions:
                self.add_inspector_row("TRANSITION COUNT", str(len(state.transitions)), row_index)
                row_index += 1
        
        return row_index

    def _handle_transition(self, current, row_index):
        row_index = self.add_category_header("Transition Details", row_index)
        
        event = current.text(0)
        self.add_inspector_row("EVENT", event, row_index)
        row_index += 1

        target_id = current.text(2)
        self.add_inspector_row("TARGET", target_id, row_index)
        row_index += 1
        
        parent = current.parent()
        if parent and parent.text(1) == "State":
            state_name = parent.text(0)
            layer_id = parent.text(2)
            
            layer = self.cafile.rootlayer.findlayer(layer_id) if layer_id else self.cafile.rootlayer
                
            if layer and hasattr(layer, 'states') and state_name in layer.states:
                state = layer.states[state_name]
                if hasattr(state, 'transitions') and event in state.transitions:
                    transition = state.transitions[event]
                    
                    if hasattr(transition, 'elements') and transition.elements:
                        row_index = self.add_category_header("Transition Elements", row_index)
                        self.add_inspector_row("ELEMENT COUNT", str(len(transition.elements)), row_index)
                        row_index += 1
        
        return row_index

    def _handle_set_value(self, current, row_index):
        row_index = self.add_category_header("Target Info", row_index)
        
        targetId = current.data(0, Qt.UserRole)
        if targetId:
            self.add_inspector_row("TARGET ID", targetId, row_index)
            row_index += 1
            
            target_layer = self.cafile.rootlayer.findlayer(targetId)
            if target_layer and hasattr(target_layer, "name"):
                self.add_inspector_row("TARGET NAME", target_layer.name, row_index)
                row_index += 1
        
        row_index = self.add_category_header("Value", row_index)
            
        keyPath = current.text(0)
        if keyPath:
            self.add_inspector_row("KEY PATH", keyPath, row_index)
            row_index += 1
            
        value = current.text(2)
        if value:
            self.add_inspector_row("VALUE", value, row_index)
            row_index += 1

    def _handle_animation(self, current, row_index):
        row_index = self.add_category_header("Animation Details", row_index)
        
        details = current.text(2)
        if details:
            for detail in details.split(", "):
                if ":" in detail:
                    key, value = detail.split(":", 1)
                    self.add_inspector_row(key.strip().upper(), value.strip(), row_index)
                    row_index += 1

    def _handle_add_animation(self, current, row_index):
        row_index = self.add_category_header("Target Info", row_index)
        
        targetId = current.text(2)
        if targetId:
            self.add_inspector_row("TARGET ID", targetId, row_index)
            row_index += 1
            
            target_layer = self.cafile.rootlayer.findlayer(targetId)
            if target_layer and hasattr(target_layer, "name"):
                self.add_inspector_row("TARGET NAME", target_layer.name, row_index)
                row_index += 1
            
        keyPath = current.text(0)
        if keyPath:
            self.add_inspector_row("KEY PATH", keyPath, row_index)
            row_index += 1
        
        parent = current.parent()
        if parent and parent.text(1) == "State":
            state_name = parent.text(0)
            layer_id = parent.text(2)
            
            if layer_id:
                layer = self.cafile.rootlayer.findlayer(layer_id)
            else:
                layer = self.cafile.rootlayer
                
            if layer and hasattr(layer, "states") and state_name in layer.states:
                state = layer.states[state_name]
                if hasattr(state, "elements"):
                    for element in state.elements:
                        if element.__class__.__name__ == "LKStateAddAnimation" and element.targetId == targetId and element.keyPath == keyPath:
                            if hasattr(element, "animations") and element.animations:
                                row_index = self.add_category_header("Animations", row_index)
                                self.add_inspector_row("ANIMATION COUNT", str(len(element.animations)), row_index)
                                row_index += 1

    def _handle_transition_element(self, current, row_index):
        row_index = self.add_category_header("Element Details", row_index)
        
        key = current.text(0)
        if key:
            self.add_inspector_row("KEY", key, row_index)
            row_index += 1
            
        targetId = current.text(2)
        if targetId:
            self.add_inspector_row("TARGET ID", targetId, row_index)
            row_index += 1
            
            target_layer = self.cafile.rootlayer.findlayer(targetId)
            if target_layer and hasattr(target_layer, "name"):
                self.add_inspector_row("TARGET NAME", target_layer.name, row_index)
                row_index += 1
    
    def onInspectorChanged(self, item):
        if item.column() != 1:
            return

        obj = getattr(self, 'currentInspectObject', None)
        if obj is None:
            return

        # --- Update data model ---
        key = self.ui.tableWidget.item(item.row(), 0).text()
        val = item.text()
        parts = key.lower().split()
        xml_key = parts[0] + ''.join(p.capitalize() for p in parts[1:])

        if not hasattr(obj, xml_key):
            xml_key = key.lower().replace(' ', '_')
            if not hasattr(obj, xml_key):
                return
        
        orig_val = getattr(obj, xml_key)
        try:
            if isinstance(orig_val, list):
                nums = re.findall(r'-?\d+\.?\d*', str(val))
                setattr(obj, xml_key, [str(n) for n in nums])
            elif isinstance(orig_val, bool):
                setattr(obj, xml_key, val.lower() in ['true', '1', 'yes'])
            elif isinstance(orig_val, int):
                setattr(obj, xml_key, int(float(val)))
            elif isinstance(orig_val, float):
                 setattr(obj, xml_key, float(val))
            else: # String or other
                setattr(obj, xml_key, val)
        except (ValueError, TypeError) as e:
            print(f"Could not update property '{xml_key}': {e}")
            setattr(obj, xml_key, orig_val)
            return

        self.markDirty()

        # --- Update preview item directly ---
        scene_item = None
        for it in self.scene.items():
            if hasattr(it, "data") and it.data(0) == obj.id:
                scene_item = it
                break
        
        if not scene_item:
            return

        self.ui.tableWidget.blockSignals(True)
        
        if xml_key == 'position':
            try:
                x, y = float(obj.position[0]), float(obj.position[1])
                scene_item.setPos(x, y)
            except (ValueError, IndexError):
                pass
        elif xml_key == 'opacity':
            try:
                scene_item.setOpacity(float(obj.opacity))
            except (ValueError, TypeError):
                pass
        elif xml_key == 'hidden':
            scene_item.setVisible(not obj.hidden)
        elif xml_key == 'transform':
            pass
        elif 'Color' in xml_key:
            self.applyStylesToItem(scene_item, obj)
        
        editable = self.scene.editableItems.get(id(scene_item))
        if editable:
            editable.updateBoundingBox()

        self.ui.tableWidget.blockSignals(False)

    def onItemMoved(self, item):
        layer_id = item.data(0)
        layer = self.cafile.rootlayer.findlayer(layer_id)
        if layer:
            pos = item.pos()
            layer.position = [str(pos.x()), str(pos.y())]
        
        if hasattr(self, 'currentInspectObject') and self.currentInspectObject == layer:
            self.ui.tableWidget.blockSignals(True)
            for r in range(self.ui.tableWidget.rowCount()):
                label = self.ui.tableWidget.item(r, 0)
                if not label:
                    continue
                key = label.text()
                if key == 'POSITION':
                    self.ui.tableWidget.item(r, 1).setText(f"{pos.x():.2f}, {pos.y():.2f}")
                    break
            self.ui.tableWidget.blockSignals(False)
        self.markDirty()

    def onItemChanging(self, item):
        """Live-update inspector during a drag/resize"""
        layer_id = item.data(0)
        layer = self.cafile.rootlayer.findlayer(layer_id)
        if hasattr(self, 'currentInspectObject') and self.currentInspectObject == layer:
            self.ui.tableWidget.blockSignals(True)
            pos = item.pos()
            for r in range(self.ui.tableWidget.rowCount()):
                label = self.ui.tableWidget.item(r, 0)
                if not label:
                    continue
                key = label.text()
                if key == 'POSITION':
                    self.ui.tableWidget.item(r, 1).setText(f"{pos.x():.2f}, {pos.y():.2f}")
                    break
            self.ui.tableWidget.blockSignals(False)

    def onTransformChanged(self, item, transform):
        layer_id = item.data(0)
        layer = self.cafile.rootlayer.findlayer(layer_id)
        if layer:
            scene_rect = item.mapToScene(item.boundingRect()).boundingRect()
            w = scene_rect.width()
            h = scene_rect.height()

            x0, y0 = (layer.bounds[0], layer.bounds[1]) if hasattr(layer, 'bounds') and len(layer.bounds) == 4 else (0,0)
            layer.bounds = [str(x0), str(y0), str(w), str(h)]
            
            layer.transform = None 
        
        if hasattr(self, 'currentInspectObject') and self.currentInspectObject == layer:
            self.ui.tableWidget.blockSignals(True)
            for r in range(self.ui.tableWidget.rowCount()):
                label = self.ui.tableWidget.item(r, 0)
                if label and label.text() == 'BOUNDS':
                    self.ui.tableWidget.item(r, 1).setText(f"0, 0, {w:.2f}, {h:.2f}")
                    break
            self.ui.tableWidget.blockSignals(False)
        self.markDirty()

    def selectLayerInTree(self, layer_id: str):
        if not hasattr(self, 'ui') or not self.ui.treeWidget:
            return
        
        iterator = QTreeWidgetItemIterator(self.ui.treeWidget)
        while iterator.value():
            item = iterator.value()
            if item and item.text(2) == layer_id:
                self.ui.treeWidget.setCurrentItem(item)
                self.openInInspector(item, 0)
                return
            iterator += 1