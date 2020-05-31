# main.py - plugins.input - SRTX plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)

def block(userinput, inputRules, block, rpack):
	passRule = False
	variables = []
	rankMod = 0

	if(len(inputRules) == 1 and inputRules[0].tag == block):
		if(userinput.rawInput in inputRules[0].children):
			passRule = True
	
	return passRule, variables, rankMod
