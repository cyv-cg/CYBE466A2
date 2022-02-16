import resource


class rule():
	def __init__(self, userAttribute, resourceAttribute, actions, constraints):
		self.usAttrib = userAttribute
		self.reAttrib = resourceAttribute
		self.actions = actions
		self.constraint = constraints
		
	