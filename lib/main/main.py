import xml.etree.ElementTree as ET
import os.path

class CGImage:
    def __init__(self, src):
        self.src = src

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

        return e



class CAFile:
    def __init__(self, path):
        self.path = path
        self.elementTree = ET.parse(os.path.join(path,"main.caml"))
        self.root = self.elementTree.getroot()
        print(self.root)
        self.rootlayer = CALayer(self.root[0])

        # TODO: parse index.xml file as well
        
    def create(self):
        tree = ET.ElementTree()
        root = ET.Element("caml")
        root.set('xmlns','http://www.apple.com/CoreAnimation/1.0')
        root.append(self.rootlayer.create())



        tree._setroot(root)
        return tree




if __name__ == "__main__":
    test = CAFile("test2.ca")
    recreate = test.create()
    recreate.write("test3.ca/test3.caml")
