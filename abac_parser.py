def parse(file):
	f = open(file, "r")
	lines = f.readlines()

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

			print(f"type={term_type}, id={id}, parameters={term_parameters}")
		else:
			print(terms)

def get_terms(line):
	try:
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