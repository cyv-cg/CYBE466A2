import re 
class rule:
	"Stores a dictionary of actions and the rules associated with them for an ABAC policy"
	pass 

	def __init__(self):
		self.actionDict = {}
		#self.ruleTupleList


	def addRule(self, ruleInfo):
		#ruleInfo should contain the whole string of a rule for the ABAC policy  
		ruleList = ruleInfo[5:len(ruleInfo)-1].split(";")
		#first is to break the subject conditions into a tuple
		#for the user tuple, I will also need a tuple for the potential grouping of values
		if len(ruleList[0].strip()) > 1:
			startIdx = ruleList[0].find("{")
			endIdx = ruleList[0].find("}")
			values = tuple(ruleList[0][startIdx+1:endIdx].split(" "))			 
			#now add the tuple for values into the tuple for subject conditions
			subjSplit = ruleList[0].strip().split(" ")
			subjTuple = (subjSplit[0], subjSplit[1], values)
		else:
			subjTuple = ()
		#second is to break the resource conditions into a tuple
		#same as the user tuple, will need a value tuple for the resources
		if len(ruleList[1].strip()) > 1:
			startIdx = ruleList[1].find("{")
			endIdx = ruleList[1].find("}")
			reValues = tuple(ruleList[1][startIdx+1:endIdx].split(" "))
			#now add the tuple for reValues into the tuple for resource conditions 
			resSplit = ruleList[1].strip().split(" ")
			resTuple = (resSplit[0], resSplit[1], reValues)
		else:
			resTuple = ()
		#now there needs to be a tuple for the actions
		if len(ruleList[2].strip()) > 1:
			actionStr = ruleList[2].strip()
			actions = tuple(actionStr[1:len(actionStr)-1].split(" ")) #the range of action str removes the "{}"
		else:
			actions = ()
		#finally, conditionals are included as tuple 
		if len(ruleList[3].strip()) > 1:
			#Python has a whole different module for regex 
			splitAt = re.search("[\[\]=>]",ruleList[3])
			splitList = re.split("[\[\]=>]",ruleList[3])
			conditions = (splitList[0].strip(), splitAt[0], splitList[1].strip())
		else:
			conditions = ()
		#Now for the creation of a tuple of tuples, which will be stored in the dictionary, with the action tuple being used to find it
		ruleTuple = (subjTuple, resTuple, actions, conditions)
		#should result in dicitonary entries of type {"action": [(tuple)]}
			#note that the tuples are in lists in case there are multiple rules that have that action associated with them
		for i in actions:
			if i in self.actionDict:
				self.actionDict[i].append(ruleTuple)
			else:
				self.actionDict.update({i: [ruleTuple]})


	def __str__(self) -> str:
		return str(self.actionDict)