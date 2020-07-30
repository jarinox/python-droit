# tools.py - tools helping droit to run itself
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os as _os
import  time as _time
import importlib as _importlib
from .models import DroitPlugin as _DroitPlugin
from .models import DroitPluginInfo as _DroitPluginInfo


def createVariables(inpVars={}, username="", droitname="Droit", userinput=None):
	"""
	Create a list of variables containing all necessary pieces of data
	for formatOut
	"""
	variables = {}
	variables["global.time"] = _time.strftime("%H:%M")
	variables["global.date"] = _time.strftime("%d.%m.%Y")
	variables["global.username"] = username
	variables["global.droitname"] = droitname
	if userinput:
		variables["global.userinput"] = userinput.rawInput
	else:
		variables["global.userinput"] = ""
	for inpVar in inpVars:
		variables["inp." + inpVar] = inpVars[inpVar]
		
	return variables


def loadPlugins(location=_os.path.dirname(__file__)+"/"):
	"""
	Loads all plugins from the given location and returns them in a
	list containing DroitPlugin items.
	"""
	plugins = []
	inList = _os.listdir(path=location+"plugins/input")
	outList = _os.listdir(path=location+"plugins/output")
	
	for name in inList:
		plugins.append(_DroitPlugin("input", name, path=location))
	
	for name in outList:
		plugins.append(_DroitPlugin("output", name, path=location))
	
	return plugins


def loadPluginInfos(location=_os.path.dirname(__file__)+"/"):
	"""
	Loads all plugin infos from the given location and returns them in a
	list containing DroitPluginInfo items.
	"""
	infos = []
	inList = _os.listdir(path=location+"plugins/input")
	outList = _os.listdir(path=location+"plugins/output")
	
	for name in inList:
		infos.append(_DroitPluginInfo("input", name, path=location))
	
	for name in outList:
		infos.append(_DroitPluginInfo("output", name, path=location))
	
	return infos
