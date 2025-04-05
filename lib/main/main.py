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
        self._content = self.element.find('{http://www.apple.com/CoreAnimation/1.0}contents')
        if self._content != None:
            if self._content.get('type') == "CGImage":
                self.content = CGImage(self._content.get('src'))
            # TODO: support more than just CGImage :skull:

        self.sublayers = {}
        self._sublayerorder = []
        self.__sublayers = self.element.find("{http://www.apple.com/CoreAnimation/1.0}sublayers")
        if self.__sublayers != None:
            for layer in self.__sublayers:
                if layer.tag == "{http://www.apple.com/CoreAnimation/1.0}CALayer":
                    self.sublayers[layer.get('id')] = CALayer(layer)
                    self._sublayerorder.append(layer.get('id'))
                # TODO: support more than just CALayer

        self.states = {}
        self._states = self.element.find("{http://www.apple.com/CoreAnimation/1.0}states")
        if self._states != None:
            for state in self._states:
                self.states[state.get("name")] = LKState(state)



    def create(self):
        e = ET.Element('CALayer')
        e.set('id' ,self.id)
        e.set('name' ,self.name)
        e.set('position', " ".join(self.position))
        e.set('bounds', " ".join(self.bounds))
        if self.hidden: e.set('hidden', true)
        if self.transform != None: e.set('transform',self.transform)
        if self.anchorPoint != None: e.set('anchorPoint',self.anchorPoint)
        
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
