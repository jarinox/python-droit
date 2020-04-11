# droit core for python
# Copyright 2020 Jakob Stolze
#
# Version              v1.0.0.1
# Date last modified   11.04.2020
# Date created         08.05.2019
# Python Version       3.x
#
# DDS Version          v1.0
#
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


import os, importlib
from droit.loader import *
from droit.tools import *
import droit.dumper
import droit.models


def useRules(rules, userinput, rpack=None):
	"""
	Uses a parsed Droit Database and runs every rule onto the userinput.
	Returns all possible DroitRulesOutput sorted by relevance.
	"""
	hits = []

	for i in range(0, len(rules)): # use all rules
		variables = {}
		ranking = 0
		blocks = []
		ruleOk = True
		for j in range(0, len(rules[i].input)):
			if not(rules[i].input[j].tag in blocks):
				blocks.append(rules[i].input[j].tag)
		
		inPlugs = os.listdir("droit/plugins/input")
		for block in blocks:			
			if(block.lower() in inPlugs):
				p = importlib.import_module("droit.plugins.input." + rules[i].input[j].tag.lower() + ".main")
				passRule, newVars, rankMod = p.block(userinput, rules[i].input, block, rpack)
				for var in newVars:
					variables[var] = newVars[var]
				if(passRule):
					ranking = ranking + rankMod
				else:
					ruleOk = False
					break
			else:
				ruleOk = False
		
		if(ruleOk):
			hits.append([rules[i].output, variables, len(userinput.words) - len(rules[i].input) + ranking])

	if(hits != []):
		hits = sorted(hits, key=lambda hit: hit[2])
	return hits



def formatOut(outputRules, variables, rpack=None):
	"""Evaluates a DroitRuleOutput"""
	output = ""
	
	for i in range(0, len(outputRules)):
		if("TEXT" == outputRules[i].tag.upper()):
			for text in outputRules[i].children:
				output += text
		
		if("VAR" == outputRules[i].tag.upper()):
			for var in variables:
				if(var in outputRules[i].children):
					output += variables[var]
		
		if("EVAL" == outputRules[i].tag.upper()):
			plugin = ""
			for plug in outputRules[i].children:
				plugin += plug
			plugin = plugin.split(".", 1)
			for var in variables:
				if("*" + var in plugin[1]):
					plugin[1] = plugin[1].replace("*" + var, "\"" + variables[var] + "\"")
			
			isMethod = False
			if("(" in plugin[1]):
				isMethod = True
				plugin.append(plugin[1].split("(")[1][:-1].replace('"', ""))
				plugin[1] = plugin[1].split("(")[0]
			
			params = []
			for i in range(2, len(plugin)):
				params.append(plugin[i])
			
			plug = importlib.import_module("droit.plugins.output." + plugin[0] + ".main")
			method = getattr(plug, plugin[1])
			
			if(isMethod):
				if(plugin[1][1] != ""):
					return method(params, rpack)
				else:
					return method(rpack)


	return output



def simpleIO(rawInput, databasePath):
	"""
	Simple function to test a database and to create simple bots.
	The use is restricted and not recommended because no resources
	can be provided. This function is intended to be used for testing.
	Use an own script to create more complex bots.
	"""
	userinput = DroitUserinput(rawInput)
	x = useRules(parseDroitXML(databasePath), userinput)
	if(x != []):
		return formatOut(x[0][0], createVariables(inpVars=x[0][1], userinput=userinput))
	else:
		return ""

