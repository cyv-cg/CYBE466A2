import abac_parser as p

class resourceAttrib():
	rid = ""

	attributes = { }

	def __init__(self, rid, attributes):
		self.rid = rid
		self.attributes = p.parse_attrib(attributes)
		print(f"resourceAttrib __init__({self.rid}, {self.attributes})")