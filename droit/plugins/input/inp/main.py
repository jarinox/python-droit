# main.py - plugins.input - INP plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

from parse import parse


def block(userinput, iN, name, db):
	pTexts = []
	passRule = False
	rankMod = 0
	varChildren = {}

	inputRules = db.rules[iN].input
	reqs = db.getPluginRequirements(name, "placeholder")

	for rule in inputRules:
		for function in reqs:
			pTexts = function(rule, pTexts)
		
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
		results = parse(pText, userinput.rawInput)
		if(results != None):
			passRule = True
			
			variables = results.__dict__["named"]
			for variable in variables:
				if("strict." in variable):
					value = variables[variable]
					if not(value in varChildren[variable]):
						passRule = False
	
	outVars = {}
	for variable in variables:
		outVars["inp."+variable.replace("strict.", "")] = variables[variable]

	return passRule, outVars, rankMod, db