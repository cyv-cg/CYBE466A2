from resourceAttrib import resourceAttrib
from userAttrib import userAttrib
import rule


def parse(file):
	f = open(file, "r")
	lines = f.readlines()

	rules = rule.rule()

	attributes = { }
	for l in lines:
		# Skip comments and blank lines.
		if l[0] == '#' or len(l.strip()) == 0:
			continue

		terms = get_terms(l)
		term_type = terms[0]


		if term_type != 'rule':
			term_parameters = terms[1]
			id = term_parameters[0]
			term_parameters = term_parameters[1:len(term_parameters)]

			if term_type == 'userAttrib':
				# attributes[id] = userAttrib(id, term_parameters)
				attributes.update({id: userAttrib(id, term_parameters)})
			elif term_type == 'resourceAttrib':
				# attributes[id] = resourceAttrib(id, term_parameters)
				attributes.update({id: resourceAttrib(id, term_parameters)})
		elif term_type == 'rule':
			rules.addRule(l)
		else:
			# print(terms)
			pass
	f.close()
	return attributes, rules

def get_terms(line):
	try:
		line = line.replace(")\n", "")
		# This should return a list with 2 elements: the type of rule or attribute, and 
		# all the stuff inside the parentheses.
		components = line.split('(')

		# The second element of 'components' should be the parameters of the constructor.
		# This string is then split at any comma followed by a space, which *should* separate
		# each parameter individually, if the formating is kept consistent with the provided files.
		parameters = components[1].split(", ")

		# Return the first element of 'components', which should be the type, followed by the parameters.
		return components[0], parameters
		
	except Exception as e:
		print(e)

def parse_attrib(attributes):
	# Initialize a dictionary for the attributes.
	att = { }
	# Process each string in the given list.
	for a in attributes:
		# Split at '=' to separate keys and values.
		comps = a.split("=")
		key = comps[0]
		val = comps[1]

		# If the value is surrounded by braces, then it is a multivalued attribute and should be assigned as a list.
		if val[0] == '{' and val[len(val)-1] == '}':
			# Remove the braces.
			val = val.replace('{', '').replace('}', '')
			# Split the value at a space to get the list of values.
			val = val.split(' ')

		att[key] = val

	return att
