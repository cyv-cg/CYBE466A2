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
			ruleSeperator = ruleList[0].split(",")
			tupleList = []
			for i in ruleSeperator:
				startIdx = i.find("{")
				endIdx = i.find("}")
				values = tuple(i[startIdx+1:endIdx].split(" "))	 
				#now add the tuple for values into the tuple for subject conditions
				subjSplit = i.strip().split(" ")
				tupleList.append((subjSplit[0], subjSplit[1], values))
			subjTuple = tuple(tupleList)
		else:
			subjTuple = (())
		#second is to break the resource conditions into a tuple
		#same as the user tuple, will need a value tuple for the resources
		if len(ruleList[1].strip()) > 1:
			ruleSeperator = ruleList[1].split(''',''')
			tupleList = []
			for i in ruleSeperator:
				startIdx = i.find("{")
				endIdx = i.find("}")
				reValues = tuple(i[startIdx+1:endIdx].split(" "))
				#now add the tuple for reValues into the tuple for resource conditions 
				resSplit = i.strip().split(" ")
				tupleList.append((resSplit[0], resSplit[1], reValues))
			resTuple = tuple(tupleList)
		else:
			resTuple = (())
		#now there needs to be a tuple for the actions
		if len(ruleList[2].strip()) > 1:
			actionStr = ruleList[2].strip()
			actions = tuple(actionStr[1:len(actionStr)-1].split(" ")) #the range of action str removes the "{}"
		else:
			actions = ()
		#finally, conditionals are included as tuple 
		if len(ruleList[3].strip()) > 1:
			ruleSeperator = ruleList[3].split(",")
			seperatedTupleList = []
			for i in ruleSeperator:
				#Python has a whole different module for regex 
				splitAt = re.search("[\[\]=>]",i)
				splitList = re.split("[\[\]=>]",i)
				seperatedTupleList.append((splitList[0].strip(), splitAt[0], splitList[1].strip()))
			conditions = tuple(seperatedTupleList)
		else:
			conditions = (())
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
		#Takes in the desired aciton, the appropriate subjectTuple and resourceTuple and will either confirm or deny the action under those circumstances
		#note that the tuples should be in form (ID, {attribute dictionary})
		if desiredAction in self.actionDict:
			possibleRule = self.actionDict[desiredAction]
		else:
			return False
		foundMatch = False
		#use foundMatch to check each possible failed condition for this action
		for i in possibleRule:
			#First checks the subject condition tuple
			if len(i[0]) > 0:
				passes = 0
				for s in i[0]:
					sAtrib = s[0] #stores the attribute to be checked
					sOp = s[1] #stores the operator to be checked with
					if sOp == '['and sAtrib in subjectDict:
						if subjectDict[sAtrib] in s[2]:
							passes += 1
					elif sOp == ']' and sAtrib in subjectDict:
						if s[2] in subjectDict[sAtrib]:
							passes +=1  
					else:
						print("\n\n---------------\nYou've found a secret, this program is broken\n----------------\n\n")
				if len(i[0]) == passes:
					foundMatch = True
			#if the subject has matched a criteria, then checks that the subject matches its criteria
			elif len(i[0]) == 0:
				foundMatch = True
			if foundMatch and len(i[1]) > 0:
				foundMatch = False
				passes = 0
				for r in i[1]:
					rAtrib = r[0] #stores attribute to be checked
					rOp = r[1]	#Stores the operator to be used
					if rOp == '[' and rAtrib in resourceDict:
						if resourceDict[rAtrib] in r[2]:
							passes +=1
					elif rOp == ']' and rAtrib in resourceDict:
						if r[2] in resourceDict[rAtrib]:
							passes +=1
					else:
						print("\n\n---------------\nYou've found a secret, this program is still broken\n----------------\n\n")
				if len(i[1]) == passes:
					foundMatch = True
			elif foundMatch and len(i[1]) == 0:
				pass
			else:
				foundMatch = False
			if foundMatch and len(i[3]) > 0: 
				foundMatch = False
				passes = 0
				for c in i[3]:
					if c[0] in subjectDict and c[2] in resourceDict:
						subjArg = subjectDict[c[0]]
						resArg = resourceDict[c[2]]
						compOp = c[1]
						if compOp == '[':
							if subjArg in resArg:
								passes +=1
						elif compOp == ']':
							if resArg in subjArg:
								passes +=1
						elif compOp == '=':
							if subjArg == resArg:
								passes +=1
						elif compOp == '>':
							subpass = 0
							for items in resArg:
								if items in subjArg:
									subpass +=1
							if len(resArg) == subpass:
								passes +=1
						else:
							print("\n\n----------------\Invalid comparison Operator \n----------------\n\n\n")
				if len(i[3]) == passes:
					foundMatch = True
			elif foundMatch and len(i[3]) == 0:
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