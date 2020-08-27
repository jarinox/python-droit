# main.py - plugins.input - SRTX plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def block(userinput, iN, block, db):
	passRule = False
	variables = []
	rankMod = 2

	inputRules = db.rules[iN].input

	if(len(inputRules) == 1 and inputRules[0].tag == block):
		if(userinput.simpleInput in inputRules[0].children):
			passRule = True
	
	return passRule, variables, rankMod, db

