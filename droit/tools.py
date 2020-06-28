# tools.py - tools helping droit to run itself
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os, time, importlib
from .models import DroitPlugin, DroitPluginInfo


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


def loadPlugins(location=os.path.dirname(__file__)+"/"):
	"""
	Loads all plugins from the given location and returns them in a
	list containing DroitPlugin items.
	"""
	plugins = []
	inList = os.listdir(path=location+"plugins/input")
	outList = os.listdir(path=location+"plugins/output")
	
	for name in inList:
		plugins.append(DroitPlugin("input", name, path=location))
	
	for name in outList:
		plugins.append(DroitPlugin("output", name, path=location))
	
	return plugins


def loadPluginInfos(location=os.path.dirname(__file__)+"/"):
	"""
	Loads all plugin infos from the given location and returns them in a
	list containing DroitPluginInfo items.
	"""
	infos = []
	inList = os.listdir(path=location+"plugins/input")
	outList = os.listdir(path=location+"plugins/output")
	
	for name in inList:
		infos.append(DroitPluginInfo("input", name, path=location))
	
	for name in outList:
		infos.append(DroitPluginInfo("output", name, path=location))
	
	return infos
