# models.py - structure python-droit data
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


import importlib, json
from droit.io import DroitIO


class DroitSettings:
	"""Read and write settings from and to config.json"""

	def __init__(self, location=""):
		self.location = location
		self.loadSettings()
	
	def loadSettings(self):
		"""load settings from config.json"""
		try:
			raw = open(self.location + "config.json", "r").read()
			self.settings = json.loads(raw)
			return True
		except:
			return False
		
	def saveSettings(self):
		"""save settings to config.json"""
		data = json.dumps(self.settings)
		open(self.location + "config.json", "w").write(data)
	
	def initSettings(self):
		"""create basic config.json file"""
		self.settings = {"username": "", "droitname": "", "ioMode": "console"}
		self.saveSettings()


class DroitCache:
	"""Cache the return value of slow functions"""
	def __init__(self):
		self.storage = []
	
	def run(self, function, param1=None, param2=None, param3=None):
		name = function.__module__ +  "." + function.__name__
		params = [param1, param2, param3]

		for item in self.storage:
			if(item["name"] == name and item["params"] == params):
				return item["value"]
			
		value = None
		if(param1 == None):
			value = function()
		elif(param2 == None):
			value = function(param1)
		elif(param3 == None):
			value = function(param1, param2)
		else:
			value = function(param1, param2, param3)
		
		self.storage.append({"name": name, "params": params, "value": value})
		return value


class DroitResourcePackage:
	"""Provides useful tools and information to any part of python-droit"""
	def __init__(self, settings=DroitSettings(), plugins=[]):
		self.tools = importlib.import_module("droit.tools")
		self.io = DroitIO()
		self.settings = settings
		self.plugins = plugins
		self.cache = DroitCache()


class DroitGmrResource:
	def __init__(self, gmrModule=None, gmrDatabase=None):
		self.gmrModule = gmrModule
		self.gmrDatabase = gmrDatabase


class DroitRuleInOut:
	"""Stores an input-rule or an output-rule"""
	def __init__(self, tag, attrib, children, mode):
		self.mode = mode
		self.tag = tag
		self.attrib = attrib
		self.children = children


class DroitRule:
	"""Stores a list of inputRules and a list of outputRules."""
	def __init__(self, inputRules, outputRules):
		self.input = inputRules
		self.output = outputRules


class DroitUserinput:
	"""
	Stores the raw userinput as well as a list of the words the userinput
	consists of. The list is created on init.
	"""
	def __init__(self, rawInput):
		self.rawInput = rawInput
		pin = rawInput
		rmchars = [",", ":", "!", ".", "-", "?", ";", "'", "\"", "(", ")", "$"]
		for i in range(0, len(rmchars)): # remove unnecessary characters
			pin = pin.replace(rmchars[i], "")
		while("  " in pin):
			pin = pin.replace("  ", " ") # double blank to single blank
		pin = pin.lower()
		self.words = pin.split(" ") # split up words at blank


class DroitPlugin:
	"""Loads a plugin."""
	def __init__(self, mode, name, path="droit/"):
		self.mode = mode.lower()
		self.name = name.lower()
		self.plugin = importlib.import_module(path.replace("/", ".") + "plugins." + mode + "." + name + ".main")
		self.info = DroitPluginInfo(mode, name, path=path)


class DroitPluginInfo:
	"""Contains information about a DroitPlugin"""
	def __init__(self, mode, name, path="droit/"):
		self.mode = mode
		self.name = name
		if(mode == "input"):
			info = json.loads(open(path+ "plugins/" + mode + "/" + name + "/info.json", "r").read())
			self.description = info["description"]
			self.attrib = info["attributes"]


class DroitSearchHit:
	"""Object returned by useRules()"""
	def __init__(self, rule, variables, ranking):
		self.rule = rule
		self.variables = variables
		self.ranking = ranking