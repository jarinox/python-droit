# main.py - plugins.input - RANK plugin for python-droit
# Copyright 2021 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def block(userinput, iN, name, db):
	rankMod = 0
	inputRules = db.rules[iN].input
	
	for rule in inputRules:
		if(rule.tag == name.upper()):
			try:
				rankMod += int(rule.children[0])
			except:
				print("python-droit: error: plugins.input.rank - invalid value")

	return True, {}, rankMod, db