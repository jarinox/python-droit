# main.py - plugins.input - INP plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)

from parse import parse


def block(userinput, inputRules, name, rpack):
	pTexts = []
	passRule = False
	rankMod = 0
	varChildren = {}

	for rule in inputRules:
		if(rule.tag == "TEXT"):
			if(pTexts == []):
				for child in rule.children:
					pTexts.append(child + " ")
			else:
				pNew = []
				for i in range(0, len(pTexts)):
					for child in rule.children:
						pNew.append(pTexts[i] + child + " ")
				pTexts = pNew
		
		if(rule.tag == name.upper()):
			varname = rule.attrib["var"]
			if(len(rule.children) > 0):
				varname = "strict." + varname
				varChildren[varname] = rule.children
			if(pTexts == []):
				pTexts.append("{" + varname + "} ")
			else:
				pcop = pTexts
				for k in range(0, len(pcop)):
					pTexts[k] = pTexts[k] + "{" + varname + "} "
	
	for i in range(0, len(pTexts)):
		if(pTexts[i][-1] == " "):
			pTexts[i] = pTexts[i][0:len(pTexts[i])-1]

	variables = {}
	for pText in pTexts:
		results = parse(pText.lower(), userinput.rawInput.lower())
		if(results != None):
			passRule = True
			rankMod = 1
			
			variables = results.__dict__["named"]
			for variable in variables:
				if("strict." in variable):
					value = variables[variable]
					if not(value in varChildren[variable]):
						passRule = False
						rankMod = 0
	
	outVars = {}
	for variable in variables:
		outVars[variable.replace("strict.", "")] = variables[variable]

	return passRule, outVars, rankMod, rpack