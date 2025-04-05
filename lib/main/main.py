import xml.etree.ElementTree as ET
import os.path
import plistlib

class CGImage:
    def __init__(self, src):
        self.src = src

class LKStateSetValue:
    def __init__(self, element):
        self.element = element
        self.targetId = self.element.get("targetId")
        self.keyPath = self.element.get("keyPath")
        self.value = self.element[0].get("value")
        self.valueType = self.element[0].get("type")
    def create(self):
        e = ET.Element('LKStateSetValue')
        e.set("targetId",self.targetId)
        e.set("keyPath",self.keyPath)
        val = ET.SubElement(e,'value')
        val.set("value",self.value)
        val.set("type",self.valueType)

        return e

class LKState:
    def __init__(self, element):
        self.element = element
        self.name = self.element.get("name")

        self.elements = []
        self._elements = self.element.find("{http://www.apple.com/CoreAnimation/1.0}elements")
        if self._elements != None:
            for element in self._elements:
                if element.tag == "{http://www.apple.com/CoreAnimation/1.0}LKStateSetValue":
                    self.elements.append(LKStateSetValue(element))
    def create(self):
        e = ET.Element('LKState')
        e.set("name",self.name)
        if self._elements != None:
            elements = ET.SubElement(e,'elements')
            for element in self.elements:
                elements.append(element.create())

        return e

class CAAnimation:
    def __init__(self):
        pass
        # placeholder for when future animations are added

class CASpringAnimation(CAAnimation):
    def __init__(self ,element):
        self.element = element
        self.type = "CASpringAnimation"
        self.damping = self.element.get("damping")
        self.mass = self.element.get("mass")
        self.stiffness = self.element.get("stiffness")
        self.velocity = self.element.get("velocity")
        self.keyPath = self.element.get("keyPath")
        self.duration = self.element.get("duration")
        self.fillMode = self.element.get("fillMode")
        self.micarecalc = self.element.get("mica_autorecalculatesDuration")
    def create(self):
        e = ET.Element("animation")
        e.set("type",self.type)
        e.set("damping",self.damping)
        e.set("mass",self.mass)
        e.set("stiffness",self.stiffness)
        e.set("velocity",self.velocity)
        e.set("keyPath",self.keyPath)
        e.set("duration",self.duration)
        e.set("fillMode",self.fillMode)
        e.set("mica_autorecalculatesDuration",self.micarecalc) # TODO: check if this is necessary

        return e

class LKStateTransitionElement:
    def __init__(self, element):
        self.element = element
        self.key = self.element.get("key")
        self.targetId = self.element.get("targetId")

        self.animations = []
        self._animations = self.element.findall("{http://www.apple.com/CoreAnimation/1.0}animation")
        if self._animations != None:
            for animation in self._animations:
                if animation.get("type") == "CASpringAnimation":
                    self.animations.append(CASpringAnimation(animation))

    def create(self):
        e = ET.Element('LKStateTransitionElement')
        e.set("key",self.key)
        e.set("targetId",self.targetId)
        if self._animations != None:
            for animation in self.animations:
                e.append(animation.create())

        return e

class LKStateTransition:
    def __init__(self,element):
        self.element = element
        self.fromState = self.element.get("fromState")
        self.toState = self.element.get("toState")

        self.elements = []
        self._elements = self.element.find("{http://www.apple.com/CoreAnimation/1.0}elements")
        if self._elements != None:
            for element in self._elements:
                self.elements.append(LKStateTransitionElement(element))
    def create(self):
        e = ET.Element('LKStateTransition')
        e.set("fromState",self.fromState)
        e.set("toState",self.toState)
        
        if self._elements != None:
            elements = ET.SubElement(e,'elements')
            for element in self.elements:
                elements.append(element.create())
        
        return e

class CANumber:
    def __init__(self, element):
        self.element = element
        self.type = self.element.tag.replace("{http://www.apple.com/CoreAnimation/1.0}","")
        self.value = self.element.get("value")
    def create(self):
        e = ET.Element(self.type)
        e.set("value",self.value)

        return e

class CAKeyframeAnimation(CAAnimation):
    def __init__(self, element):
        self.element = element
        self.tag = self.element.tag.replace("{http://www.apple.com/CoreAnimation/1.0}","") # either animation or p i think
        if self.tag == "p": self.key = self.element.get("key")
        self.type="CAKeyframeAnimation"
        self.calculationMode = self.element.get("calculationMode")
        self.keyPath = self.element.get("keyPath")
        self.beginTime = self.element.get("beginTime")
        self.duration = self.element.get("duration")
        self.fillMode = self.element.get("fillMode")
        self.removedOnCompletion = self.element.get("removedOnCompletion")
        self.repeatCount = self.element.get("repeatCount")
        self.speed = self.element.get("speed")

        self.keyTimes = []
        self._keyTimes = self.element.find("{http://www.apple.com/CoreAnimation/1.0}keyTimes")
        if self._keyTimes != None:
            for keyTime in self._keyTimes:
                self.keyTimes.append(CANumber(keyTime))

        self.values = []
        self._values = self.element.find("{http://www.apple.com/CoreAnimation/1.0}values")
        if self._values != None:
            for value in self._values:
                self.values.append(CANumber(value))

    def create(self):
        e = ET.Element(self.tag)

        e.set("type","CAKeyframeAnimation")
        if self.tag == "p": e.set("key",self.key)
        e.set("calculationMode",self.calculationMode)
        e.set("keyPath", self.keyPath)
        e.set("beginTime", self.beginTime)
        e.set("duration",self.duration)
        e.set("fillMode",self.fillMode)
        e.set("removedOnCompletion", self.removedOnCompletion)
        e.set("repeatCount", self.repeatCount)
        e.set("speed", self.speed)

        if self.keyTimes != []:
            keyTimes = ET.SubElement(e,'keyTimes')
            for keyTime in self.keyTimes:
                keyTimes.append(keyTime.create())

        if self.values != []:
            values = ET.SubElement(e,'values')
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
        self._content = self.element.find('{http://www.apple.com/CoreAnimation/1.0}contents')
        if self._content != None:
            if self._content.get('type') == "CGImage":
                self.content = CGImage(self._content.get('src'))
            # TODO: support more than just CGImage :skull:

        self.sublayers = {}
        self._sublayerorder = []
        self._sublayers = self.element.find("{http://www.apple.com/CoreAnimation/1.0}sublayers")
        if self._sublayers != None:
            for layer in self._sublayers:
                if layer.tag == "{http://www.apple.com/CoreAnimation/1.0}CALayer":
                    self.sublayers[layer.get('id')] = CALayer(layer)
                    self._sublayerorder.append(layer.get('id'))
                # TODO: support more than just CALayer

        self.states = {}
        self._states = self.element.find("{http://www.apple.com/CoreAnimation/1.0}states")
        if self._states != None:
            for state in self._states:
                self.states[state.get("name")] = LKState(state)

        self.stateTransitions = []
        self._stateTransitions = self.element.find("{http://www.apple.com/CoreAnimation/1.0}stateTransitions")
        if self._stateTransitions != None:
            for transition in self._stateTransitions:
                self.stateTransitions.append(LKStateTransition(transition))

        self.animations = []
        self._animations = self.element.find("{http://www.apple.com/CoreAnimation/1.0}animations")
        if self._animations != None:
            for animation in self._animations:
                if animation.get("type") == "CAKeyframeAnimation":
                    self.animations.append(CAKeyframeAnimation(animation))



    def create(self):
        e = ET.Element('CALayer')
        e.set('id' ,self.id)
        e.set('name' ,self.name)
        e.set('position', " ".join(self.position))
        e.set('bounds', " ".join(self.bounds))
        if self.hidden: e.set('hidden', True)
        if self.transform != None: e.set('transform',self.transform)
        if self.anchorPoint != None: e.set('anchorPoint',self.anchorPoint)
        if self.geometryFlipped != None: e.set('geometryFlipped',self.geometryFlipped)
        
        if self._content != None:
            content = ET.SubElement(e,'contents')
            if type(self.content) == CGImage:
                content.set('type','CGImage')
                content.set('src',self.content.src)

        if len(self._sublayerorder) > 0:
            sublayers = ET.SubElement(e,'sublayers')
            for layer in self._sublayerorder:
                sublayers.append(self.sublayers.get(layer).create())

        if self.states != {}:
            states = ET.SubElement(e,'states')
            for _,state in self.states.items():
                states.append(state.create())

        if self.stateTransitions != []:
            stateTransitions = ET.SubElement(e,'stateTransitions')
            for stateTransition in self.stateTransitions:
                stateTransitions.append(stateTransition.create())


        if self.animations != []:
            animations = ET.SubElement(e,'animations')
            for animation in self.animations:
                animations.append(animation.create())

        return e



class CAFile:
    def __init__(self, path):
        self.path = path
        # parse index.xml because it tells you the name of the .caml file
        self.assets = {}
        with open(os.path.join(path,"index.xml"),'rb') as f:
            self.index = plistlib.load(f,fmt=plistlib.FMT_XML)
            f.close()

        if os.path.exists(os.path.join(path,"assets")):
            for asset in os.listdir(os.path.join(path,"assets")):
                with open(os.path.join(path,"assets",asset),"rb") as f:
                    val = f.read()
                    self.assets[os.path.basename(f.name)] = val
                    f.close()



        self.elementTree = ET.parse(os.path.join(path,self.index["rootDocument"]))
        self.root = self.elementTree.getroot()
        self.rootlayer = CALayer(self.root[0])


    def create(self):
        tree = ET.ElementTree()
        root = ET.Element("caml")
        root.set('xmlns','http://www.apple.com/CoreAnimation/1.0')
        root.append(self.rootlayer.create())

        tree._setroot(root)
        return tree

    def write_file(self,filename,path="./"):
        capath = os.path.join(path,filename)
        if not os.path.exists(capath):
            os.makedirs(capath)
        with open(os.path.join(capath,'index.xml'),'wb') as f:
            plistlib.dump(self.index,f,fmt=plistlib.FMT_XML)
            f.close()
        
        if len(self.assets) > 0:
            assetspath = os.path.join(capath,"assets")
            if not os.path.exists(assetspath):
                os.makedirs(assetspath)
            for asset in self.assets:
                with open(os.path.join(assetspath,asset), 'wb') as f:
                    f.write(self.assets[asset])
                    f.close()

        self.create().write(os.path.join(capath,self.index['rootDocument']))






if __name__ == "__main__":
    test = CAFile("test2.ca")
    test.write_file("test3.ca")
