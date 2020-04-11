# tools.py - tools helping droit to run itself
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


import os, time, json, importlib


class SettingsObject:
	def __init__(self):
		self.loadSettings()
	
	def loadSettings(self):
		raw = open("config.json", "r").read()
		self.settings = json.loads(raw)
		
	def saveSettings(self):
		data = json.dumps(self.settings)
		open("config.json", "w").write(data)
	
	def initSettings(self):
		self.settings = {"username": "", "droitname": "", "ioMode": "console"}
		self.saveSettings()


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
