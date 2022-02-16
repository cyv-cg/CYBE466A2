import abac_parser as p

class userAttrib():
	uid = ""

	attributes = { }

	def __init__(self, uid, attributes):
		self.uid = uid
		self.attributes = p.parse_attrib(attributes)
		print(f"userAttrib __init__({self.uid}, {self.attributes})")