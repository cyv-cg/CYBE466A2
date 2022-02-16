class userAttrib():
	uid = ""

	def __init__(self, uid, parameters):
		self.uid = uid
		print(f"userAttrib __init__({uid}, {parameters})")