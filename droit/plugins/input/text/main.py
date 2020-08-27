# main.py - plugins.input - TEXT plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def block(userinput, iN, block, db):
	passRule = True
	variables = []
	rankMod = 1

	inputRules = db.rules[iN].input
	
	for j in range(0, len(inputRules)):
		if(block == inputRules[j].tag):
			dont = False
			if "not" in inputRules[j].attrib:
				dont = (inputRules[j].attrib["not"] == "true")
				if(dont):
					rankMod = 2
			
			thisRule = False
			for i in range(0, len(inputRules[j].children)):
				if(inputRules[j].children[i].split(" ") == 1):
					if(inputRules[j].children[i] in userinput.words and not(dont)):
						thisRule = True
					if(not(inputRules[j].children[i] in userinput.words) and dont):
						thisRule = True
				else:
					if(inputRules[j].children[i] in userinput.simpleInput and not(dont)):
						thisRule = True
					if(not(inputRules[j].children[i] in userinput.simpleInput) and dont):
						thisRule = True
			
			if not(thisRule):
				passRule = False
	
	return passRule, variables, rankMod, db
