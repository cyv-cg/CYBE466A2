import abac_parser as p

class resourceAttrib():

	attributes = { }

	def __init__(self, rid, attributes):
		self.attributes = p.parse_attrib(attributes)
		self.attributes['rid'] = rid
		# print(f"resourceAttrib __init__({self.attributes['rid']}, {self.attributes})")