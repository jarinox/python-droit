# tools.py - tools helping droit to run itself
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


import os, time, importlib
from droit.models import DroitPlugin


def createVariables(inpVars={}, username="", droitname="Droit", userinput=""):
	"""
	Create a list of variables containing all necessary pieces of data
	for formatOut
	"""
	variables = {}
	variables["global.time"] = time.strftime("%H:%M")
	variables["global.date"] = time.strftime("%d.%m.%Y")
	variables["global.username"] = username
	variables["global.droitname"] = droitname
	variables["global.userinput"] = userinput.rawInput
	for inpVar in inpVars:
		variables["inp." + inpVar] = inpVars[inpVar]
		
	return variables


def loadPlugins(location="droit/"):
	"""
	Loads all plugins from the given location and returns them in a
	list containing DroitPlugin items.
	"""
	plugins = []
	inList = os.listdir(path=location+"plugins/input")
	outList = os.listdir(path=location+"plugins/output")
	
	for name in inList:
		plugins.append(DroitPlugin("input", name))
	
	for name in outList:
		plugins.append(DroitPlugin("output", name))
	
	return plugins
