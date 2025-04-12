import xml.etree.ElementTree as ET
import os.path
import plistlib


class CGImage:
    def __init__(self, src):
        self.src = src


class CGPoint:
    def __init__(self, element):
        self.element = element
        self.type = self.element.tag.replace(
            "{http://www.apple.com/CoreAnimation/1.0}", "")
        self.value = self.element.get("value")

    def create(self):
        e = ET.Element(self.type)
        e.set("value", self.value)

        return e


class LKStateSetValue:
    def __init__(self, element):
        self.element = element
        self.targetId = self.element.get("targetId")
        self.keyPath = self.element.get("keyPath")
        self.value = self.element[0].get("value")
        self.valueType = self.element[0].get("type")

    def create(self):
        e = ET.Element('LKStateSetValue')
        e.set("targetId", self.targetId)
        e.set("keyPath", self.keyPath)
        val = ET.SubElement(e, 'value')
        val.set("value", self.value)
        val.set("type", self.valueType)

        return e


class LKState:
    def __init__(self, element):
        self.element = element
        self.name = self.element.get("name")

        self.elements = []
        self._elements = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}elements")
        if self._elements is not None:
            for element in self._elements:
                if element.tag == "{http://www.apple.com/CoreAnimation/1.0}LKStateSetValue":
                    self.elements.append(LKStateSetValue(element))

    def create(self):
        e = ET.Element('LKState')
        e.set("name", self.name)
        if self._elements is not None:
            elements = ET.SubElement(e, 'elements')
            for element in self.elements:
                elements.append(element.create())

        return e


class CAAnimation:
    def __init__(self, element):
        self.element = element
        self.tag = self.element.tag.replace(
            "{http://www.apple.com/CoreAnimation/1.0}", "")
        self.type = "CAAnimation"

        # BASIC
        self.keyPath = self.element.get("keyPath") or "position"

        # TIMING
        self.beginTime = self.element.get("beginTime")
        self.duration = self.element.get("duration")
        self.fillMode = self.element.get("fillMode")
        self.removedOnCompletion = self.element.get("removedOnCompletion")
        self.repeatCount = self.element.get("repeatCount")
        self.repeatDuration = self.element.get("repeatDuration")
        self.speed = self.element.get("speed")
        self.timeOffset = self.element.get("timeOffset")
        self.timingFunction = self.element.get("timingFunction")

    def create(self):
        e = ET.Element(self.tag)
        self.setValue(e, "type", self.type)

        # BASIC
        self.setValue(e, "keyPath", self.keyPath)

        # TIMING
        self.setValue(e, "beginTime", self.beginTime)
        self.setValue(e, "duration", self.duration)
        self.setValue(e, "fillMode", self.fillMode)
        self.setValue(e, "removedOnCompletion", self.removedOnCompletion)
        self.setValue(e, "repeatCount", self.repeatCount)
        self.setValue(e, "repeatDuration", self.repeatDuration)
        self.setValue(e, "speed", self.speed)
        self.setValue(e, "timeOffset", self.timeOffset)
        self.setValue(e, "timingFunction", self.timingFunction)

        return e

    def setValue(self, element, key, value):
        if value is not None:
            element.set(key, value)


class CASpringAnimation(CAAnimation):
    def __init__(self, element):
        super().__init__(element)
        self.type = "CASpringAnimation"

        # SPRING
        self.damping = self.element.get("damping")
        self.mass = self.element.get("mass")
        self.stiffness = self.element.get("stiffness")
        self.velocity = self.element.get("velocity")
        self.micarecalc = self.element.get("mica_autorecalculatesDuration")

    def create(self):
        e = super().create()

        # SPRING
        self.setValue(e, "damping", self.damping)
        self.setValue(e, "mass", self.mass)
        self.setValue(e, "stiffness", self.stiffness)
        self.setValue(e, "velocity", self.velocity)
        # TODO: check if this is necessary
        self.setValue(e, "mica_autorecalculatesDuration", self.micarecalc)

        return e


class CAMatchMoveAnimation(CAAnimation):
    def __init__(self, element):
        super().__init__(element)
        self.type = "CAMatchMoveAnimation"

        # MATCH MOVE
        self.additive = self.element.get("additive")
        self.appliesX = self.element.get("appliesX")
        self.appliesY = self.element.get("appliesY")
        self.appliesScale = self.element.get("appliesScale")
        self.appliesRotation = self.element.get("appliesRotation")
        self.targetsSuperlayer = self.element.get("targetsSuperlayer")
        self.usesNormalizedCoordinates = self.element.get(
            "usesNormalizedCoordinates")

        self.sourceLayer = None
        self._sourceLayer = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}sourceLayer")
        if self._sourceLayer is not None:
            self.sourceLayer = self._sourceLayer

        self.sourcePoints = []
        self._sourcePoints = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}sourcePoints")
        if self._sourcePoints != []:
            for sourcePoint in self._sourcePoints:
                self.sourcePoints.append(CGPoint(sourcePoint))

        self.animationType = None
        self._animationType = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}animationType")
        if self._animationType is not None:
            self.animationType = self._animationType

    def create(self):
        e = super().create()

        # MATCH MOVE
        self.setValue(e, "additive", self.additive)
        self.setValue(e, "appliesX", self.appliesX)
        self.setValue(e, "appliesY", self.appliesY)
        self.setValue(e, "appliesScale", self.appliesScale)
        self.setValue(e, "appliesRotation", self.appliesRotation)
        self.setValue(e, "targetsSuperLayer", self.targetsSuperlayer)
        self.setValue(e, "usesNormalizedCoordinates",
                      self.usesNormalizedCoordinates)

        if self.sourceLayer is not None:
            sourceLayer = ET.SubElement(e, "sourceLayer")
            self.setValue(sourceLayer, "object",
                          self.sourceLayer.get("object"))

        if self.sourcePoints != []:
            sourcePoints = ET.SubElement(e, "sourcePoints")
            for sourcePoint in self.sourcePoints:
                sourcePoints.append(sourcePoint.create())

        if self.animationType is not None:
            ET.SubElement(e, "animationType")

        return e


class LKStateTransitionElement:
    def __init__(self, element):
        self.element = element
        self.key = self.element.get("key")
        self.targetId = self.element.get("targetId")

        self.animations = []
        self._animations = self.element.findall(
            "{http://www.apple.com/CoreAnimation/1.0}animation")
        if self._animations is not None:
            for animation in self._animations:
                if animation.get("type") == "CASpringAnimation":
                    self.animations.append(CASpringAnimation(animation))

    def create(self):
        e = ET.Element('LKStateTransitionElement')
        e.set("key", self.key)
        e.set("targetId", self.targetId)
        if self._animations is not None:
            for animation in self.animations:
                e.append(animation.create())

        return e


class LKStateTransition:
    def __init__(self, element):
        self.element = element
        self.fromState = self.element.get("fromState")
        self.toState = self.element.get("toState")

        self.elements = []
        self._elements = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}elements")
        if self._elements is not None:
            for element in self._elements:
                self.elements.append(LKStateTransitionElement(element))

    def create(self):
        e = ET.Element('LKStateTransition')
        e.set("fromState", self.fromState)
        e.set("toState", self.toState)

        if self._elements is not None:
            elements = ET.SubElement(e, 'elements')
            for element in self.elements:
                elements.append(element.create())

        return e


class CANumber:
    def __init__(self, element):
        self.element = element
        self.type = self.element.tag.replace(
            "{http://www.apple.com/CoreAnimation/1.0}", "")
        self.value = self.element.get("value")

    def create(self):
        e = ET.Element(self.type)
        e.set("value", self.value)

        return e


class CAKeyframeAnimation(CAAnimation):
    def __init__(self, element):
        super().__init__(element)
        if self.tag == "p":
            self.key = self.element.get("key")
        self.type = "CAKeyframeAnimation"

        # KEYFRAME
        self.calculationMode = self.element.get("calculationMode")

        self.keyTimes = []
        self._keyTimes = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}keyTimes")
        if self._keyTimes is not None:
            for keyTime in self._keyTimes:
                self.keyTimes.append(CANumber(keyTime))

        self.values = []
        self._values = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}values")
        if self._values is not None:
            for value in self._values:
                self.values.append(CANumber(value))

    def create(self):
        e = super().create()
        if self.tag == "p":
            self.setValue(e, "key", self.key)

        # KEYFRAME
        self.setValue(e, "calculationMode", self.calculationMode)

        if self.keyTimes != []:
            keyTimes = ET.SubElement(e, 'keyTimes')
            for keyTime in self.keyTimes:
                keyTimes.append(keyTime.create())

        if self.values != []:
            values = ET.SubElement(e, 'values')
            for value in self.values:
                values.append(value.create())

        return e


class CALayer:
    def __init__(self, element):
        self.element = element
        self.id = self.element.get('id')
        self.name = self.element.get('name')
        self.position = self.element.get('position').split(" ")
        self.bounds = self.element.get('bounds').split(" ")
        self.hidden = True if self.element.get('hidden') == 0 else False
        self.transform = self.element.get('transform')
        self.anchorPoint = self.element.get('anchorPoint')
        self.geometryFlipped = self.element.get('geometryFlipped')
        self._content = self.element.find(
            '{http://www.apple.com/CoreAnimation/1.0}contents')
        if self._content is not None:
            if self._content.get('type') == "CGImage":
                self.content = CGImage(self._content.get('src'))
            # TODO: support more than just CGImage :skull:

        self.sublayers = {}
        self._sublayerorder = []
        self._sublayers = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}sublayers")
        if self._sublayers is not None:
            for layer in self._sublayers:
                if layer.tag == "{http://www.apple.com/CoreAnimation/1.0}CALayer":
                    self.sublayers[layer.get('id')] = CALayer(layer)
                    self._sublayerorder.append(layer.get('id'))
                # TODO: support more than just CALayer

        self.states = {}
        self._states = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}states")
        if self._states is not None:
            for state in self._states:
                self.states[state.get("name")] = LKState(state)

        self.stateTransitions = []
        self._stateTransitions = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}stateTransitions")
        if self._stateTransitions is not None:
            for transition in self._stateTransitions:
                self.stateTransitions.append(LKStateTransition(transition))

        self.animations = []
        self._animations = self.element.find(
            "{http://www.apple.com/CoreAnimation/1.0}animations")
        if self._animations is not None:
            for animation in self._animations:
                if animation.get("type") == "CAKeyframeAnimation":
                    self.animations.append(CAKeyframeAnimation(animation))
                elif animation.get("type") == "CAMatchMoveAnimation":
                    self.animations.append(CAMatchMoveAnimation(animation))

    def findlayer(self, uniqueid):
        # must be a unique value or it will return the first instance it finds because im too lazy - retron
        for id in self._sublayerorder:
            possiblelayer = self.sublayers.get(id)
            if possiblelayer.id == uniqueid:
                return possiblelayer
            else:
                if possiblelayer._sublayerorder is not []:
                    recursion = possiblelayer.findlayer(uniqueid)
                    if recursion is not None:
                        return recursion
        # if nothing is found
        return None

    def findanimation(self, keyPath):
        # this will only return first animation with a certain keyPath (not sure if its valid for multiple to exist) - retron
        for animation in self.animations:
            if animation.keyPath == keyPath:
                return animation
        # none are found
        return None

    def create(self):
        e = ET.Element('CALayer')
        e.set('id', self.id)
        e.set('name', self.name)
        e.set('position', " ".join(self.position))
        e.set('bounds', " ".join(self.bounds))
        if self.hidden:
            e.set('hidden', True)
        if self.transform is not None:
            e.set('transform', self.transform)
        if self.anchorPoint is not None:
            e.set('anchorPoint', self.anchorPoint)
        if self.geometryFlipped is not None:
            e.set('geometryFlipped', self.geometryFlipped)

        if self._content is not None:
            content = ET.SubElement(e, 'contents')
            if isinstance(self.content, CGImage):
                content.set('type', 'CGImage')
                content.set('src', self.content.src)

        if len(self._sublayerorder) > 0:
            sublayers = ET.SubElement(e, 'sublayers')
            for layer in self._sublayerorder:
                sublayers.append(self.sublayers.get(layer).create())

        if self.states != {}:
            states = ET.SubElement(e, 'states')
            for _, state in self.states.items():
                states.append(state.create())

        if self.stateTransitions != []:
            stateTransitions = ET.SubElement(e, 'stateTransitions')
            for stateTransition in self.stateTransitions:
                stateTransitions.append(stateTransition.create())

        if self.animations != []:
            animations = ET.SubElement(e, 'animations')
            for animation in self.animations:
                animations.append(animation.create())

        return e


class CAFile:
    def __init__(self, path):
        self.path = path
        # parse index.xml because it tells you the name of the .caml file
        self.assets = {}
        with open(os.path.join(path, "index.xml"), 'rb') as f:
            self.index = plistlib.load(f, fmt=plistlib.FMT_XML)
            f.close()

        if os.path.exists(os.path.join(path, "assets")):
            for asset in os.listdir(os.path.join(path, "assets")):
                with open(os.path.join(path, "assets", asset), "rb") as f:
                    val = f.read()
                    self.assets[os.path.basename(f.name)] = val
                    f.close()

        self.elementTree = ET.parse(
            os.path.join(path, self.index["rootDocument"]))
        self.root = self.elementTree.getroot()
        self.rootlayer = CALayer(self.root[0])

    def create(self):
        tree = ET.ElementTree()
        root = ET.Element("caml")
        root.set('xmlns', 'http://www.apple.com/CoreAnimation/1.0')
        root.append(self.rootlayer.create())

        tree._setroot(root)
        return tree

    def write_file(self, filename, path="./"):
        capath = os.path.join(path, filename)
        if not os.path.exists(capath):
            os.makedirs(capath)
        with open(os.path.join(capath, 'index.xml'), 'wb') as f:
            plistlib.dump(self.index, f, fmt=plistlib.FMT_XML)
            f.close()

        if len(self.assets) > 0:
            assetspath = os.path.join(capath, "assets")
            if not os.path.exists(assetspath):
                os.makedirs(assetspath)
            for asset in self.assets:
                with open(os.path.join(assetspath, asset), 'wb') as f:
                    f.write(self.assets[asset])
                    f.close()

        self.create().write(os.path.join(capath, self.index['rootDocument']))


if __name__ == "__main__":
    test = CAFile("test2.ca")
    layer = test.rootlayer.findlayer("KANYE WEST")
    layer.name = "THIS WAS EDITED"
    test.write_file("test3.ca")
