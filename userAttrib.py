import abac_parser as p

class userAttrib():
	attributes = { }

	def __init__(self, uid, attributes):
		self.attributes = p.parse_attrib(attributes)
		self.attributes['uid'] = uid
		print(f"userAttrib __init__({self.attributes['uid']}, {self.attributes})")