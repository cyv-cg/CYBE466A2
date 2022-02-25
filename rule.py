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


	def ruleCheck(self, desiredAction, subjectDict, resourceDict):
		#Takes in the desired aciton, the appropriate subjectDictionary and resourceDictionary and will either confirm or deny the action under those circumstances
		if desiredAction in self.actionDict:
			possibleRule = self.actionDict[desiredAction]
		else:
			return False
		foundMatch = False
		#use foundMatch to check each possible failed condition for this action
		for i in possibleRule:
			#First checks the subject condition
			if len(i[0]) >= 3:
				sAtrib = i[0][0] #stores the attribute to be checked
				sOp = i[0][1] #stores the operator to be checked with
				if sOp == '[':
					if subjectDict[sAtrib] in i[0][2]:
						foundMatch = True
				elif sOp == ']':
					if i[0][2] in subjectDict[sAtrib]:
						foundMatch = True 
				else:
					print("\n\n---------------\nYou've found a secret, this program is broken\n----------------\n\n")
			#if the subject has matched a criteria, then checks that the subject matches its criteria
			else:
				foundMatch = True
			if foundMatch and len(i[1]) >=3:
				foundMatch = False
				rAtrib = i[1][0] #stores attribute to be checked
				rOp = i[1][1]	#Stores the operator to be used
				if rOp == '[':
					if resourceDict[rAtrib] in i[1][2]:
						foundMatch = True
				elif rOp == ']':
					if i[1][2] in resourceDict[rAtrib]:
						foundMatch = True 
				else:
					print("\n\n---------------\nYou've found a secret, this program is still broken\n----------------\n\n")
			elif foundMatch:
				pass
			else:
				foundMatch = False
			if foundMatch and len(i[3]) >= 3:
				foundMatch = False
				compOp = i[3][1]
				if compOp == '[':
					if subjectDict[i[3][0]] in resourceDict[i[3][2]]:
						foundMatch = True
				elif compOp == ']':
					if resourceDict[i[3][2]] in subjectDict[i[3][0]]:
						foundMatch = True
				elif compOp == '=':
					if subjectDict[i[3][0]] == resourceDict[i[3][2]]:
						foundMatch = True
				elif compOp == '>':
					foundMatch = True
					for items in subjectDict[i[3][0]]:
						if items not in resourceDict[i[3][2]]:
							foundMatch = False
				else:
					print("\n\n----------------\Invalid comparison Operator \n----------------\n\n\n")
			elif foundMatch:
				pass
			else:
				foundMatch = False
			#Will return true if all conditions are met
			if foundMatch:
				return True
		#only gets here if there is not matching rule for that action
		return False



	def __str__(self) -> str:
		return str(self.actionDict)