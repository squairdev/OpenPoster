# Use to generate xml for reference frames assets folder

class XmlGenerator:
	def __init__(self):
		self.startTag = '<CGImage src="assets/'
		self.endTag = '"/>'

	def make_xml(
			self,
			startFrame = 0,
			endFrame = 1,
			filePrefix = '',
			fileExtension = '.png',
			padding = 4,
			exportAsAnimation = False,
			Fps = 30
		):
		"""
			Generate multi-line xml thingy that you can insert into .caml file directly
			if you don't provide anything it'll just use the default
		"""
		xml = []

		for i in range(startFrame, endFrame):
			number = f"{i:0{padding}d}"
			line = f"{self.startTag}{filePrefix}{number}{fileExtension}"
			xml.append(f"			{line}{self.endTag}")

		#<animations>
		#	<animation type="CAKeyframeAnimation" calculationMode="discrete" keyPath="contents" beginTime="1e-100" duration="5" removedOnCompletion="0" repeatCount="inf" repeatDuration="0" speed="1" timeOffset="0">
		#		<values>
		#			...
		#		</values>
		#	</animation>
		#</animations>

		if exportAsAnimation:
			totalDuration = (endFrame - startFrame) / Fps

			xml.insert(0, '<animations>')
			xml.insert(1, f'	<animation type="CAKeyframeAnimation" calculationMode="discrete" keyPath="contents" beginTime="1e-100" duration="{totalDuration}" removedOnCompletion="0" repeatCount="inf" repeatDuration="0" speed="1" timeOffset="0">')
			xml.insert(2, '		<values>')

			xml.append('		</values>')
			xml.append('	</animation>')
			xml.append('</animations>')

		xml = "\n".join(xml)
		
		return xml

# for debugging
if __name__ == "__main__":
	gen = XmlGenerator()
	print(gen.make_xml(0, 90, 'export_', '.jpg', 3, True, 15))