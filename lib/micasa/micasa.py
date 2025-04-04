import xml.etree.ElementTree as et
import xml.dom.minidom as minidom

# Use to generate xml for reference frames assets folder
class XmlGenerator:
	def __init__(self):
		self.startTag = 'CGImage'
		self.endTag = '/>'

	def make_xml(
			self,
			startFrame = 0,
			endFrame = 1,
			filePrefix = '',
			fileExtension = '.png',
			padding = 4,
			exportAsAnimation = False,
			fps = 30
		):
		"""
			Generate multi-line xml thingy that you can insert into .caml file directly
			if you don't provide anything it'll just use the default
		"""
		root = et.Element('root')

		#<animations>
		#	<animation type="CAKeyframeAnimation" calculationMode="discrete" keyPath="contents" beginTime="1e-100" duration="5" removedOnCompletion="0" repeatCount="inf" repeatDuration="0" speed="1" timeOffset="0">
		#		<values>
		#			...
		#		</values>
		#	</animation>
		#</animations>

		if exportAsAnimation:
			totalDuration = (endFrame - startFrame) / fps
			animations = et.SubElement(root, 'animations')
			animation = et.SubElement(animations, 'animation', {
				'type': 'CAKeyframeAnimation',
				'calculationMode': 'discrete',
				'keyPath': 'contents',
				'beginTime': '1e-100',
				'duration': str(totalDuration),
				'removedOnCompletion': '0',
				'repeatCount': 'inf',
				'repeatDuration': '0',
				'speed': '1',
				'timeOffset': '0'
			})
			values = et.SubElement(animation, 'values')

		for i in range(startFrame, endFrame):
			n = f"{i:0{padding}d}"

			if exportAsAnimation:
				asset = et.SubElement(values, self.startTag)
			else:
				asset = et.SubElement(root, self.startTag)

			asset.set('scr', f"assets/{filePrefix}{n}{fileExtension}")

		tree = et.ElementTree(root)
		return tree

# for debugging
#if __name__ == "__main__":
#	gen = XmlGenerator()
#	t = gen.make_xml(0, 30, 'test_', '.jpg', 3, True, 12)
#	xml_str = et.tostring(t.getroot(), 'utf-8')
#	formatted = minidom.parseString(xml_str).toprettyxml("\t")
#	print(formatted)
