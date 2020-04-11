# main.py - plugins.input - INP plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)

from parse import parse


def block(userinput, inputRules, block, rpack):
	pTexts = []
	passRule = False
	rankMod = 0
	
	for j in range(0, len(inputRules)):
		if(inputRules[j].tag == "TEXT"):
			if(len(inputRules[j].children) == 1):
				if(pTexts == []):
					pTexts.append(inputRules[j].children[0] + " ")
				else:
					for i in range(0, len(pTexts)):
						pTexts[i] = pTexts[i] + inputRules[j].children[0] + " "
			else:
				if(pTexts == []):
					for child in inputRules[j].children:
						pTexts.append(child + " ")
				else:
					for i in range(0, len(pTexts)):
						for child in inputRules[j].children:
							pTexts.append(pTexts[i] + child + " ")
						pTexts.remove(pTexts[i])
					
				
		if(inputRules[j].tag == "INP"):
			if(j == 0):
				pTexts.append("{" + inputRules[j].attrib["var"] + "} ")
			else:
				pcop = pTexts
				for k in range(0, len(pcop)):
					pTexts[k] = pTexts[k] + "{" + inputRules[j].attrib["var"] + "} "
	
	for i in range(0, len(pTexts)):
		if(pTexts[i][-1] == " "):
			pTexts[i] = pTexts[i][0:len(pTexts[i])-1]
	
	variables = {}
	for pText in pTexts:
		results = parse(pText.lower(), userinput.rawInput.lower())
		if(results != None):
			passRule = True
			variables = results.__dict__["named"]
			rankMod = 1
	
	return passRule, variables, rankMod
