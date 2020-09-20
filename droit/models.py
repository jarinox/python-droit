# models.py - structure python-droit data
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os as _os
import importlib as _importlib
import json as _json


class DroitSettings:
	"""Read and write settings from and to config.json"""

	def __init__(self, location=_os.path.dirname(__file__)+"/config.json"):
		self.location = location
		self.settings = {"droitname": "Droit", "ioMode": "console", "username":""}
	
	def loadSettings(self):
		"""load settings from config.json"""
		try:
			raw = open(self.location, "r").read()
			self.settings = _json.loads(raw)
			return True
		except:
			return False
		
	def saveSettings(self):
		"""save settings to config.json"""
		data = _json.dumps(self.settings)
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


class DroitRuleInput:
	"""Stores an input-rule"""
	def __init__(self, tag: str, attrib: dict, children: list):
		self.mode = "input"
		self.tag = tag.upper()
		self.attrib = attrib
		self.children = children


class DroitRuleOutput:
	"""Stores an output-rule"""
	def __init__(self, tag: str, children: list):
		self.mode = "input"
		self.tag = tag.upper()
		self.children = children


class DroitRule:
	"""Stores a list of inputRules and a list of outputRules."""
	def __init__(self, inputRules: list, outputRules: list):
		self.input = inputRules
		self.output = outputRules


class DroitUserinput:
	"""
	Stores the raw userinput as well as a list of the words the userinput
	consists of. The list is created on init.
	"""
	def __init__(self, rawInput: str):
		self.rawInput = rawInput
		pin = rawInput
		rmchars = [",", ":", "!", ".", "-", "?", ";", "'", "\"", "(", ")", "$"]
		for i in range(0, len(rmchars)): # remove unnecessary characters
			pin = pin.replace(rmchars[i], "")
		while("  " in pin):
			pin = pin.replace("  ", " ") # double blank to single blank
		self.simpleInput = pin.lower()
		self.words = self.simpleInput.split(" ") # split up words at blank


class DroitPlugin:
	"""Loads a plugin."""
	def __init__(self, mode: str, name: str, path=_os.path.dirname(__file__)+"/plugins"):
		self.mode = mode.lower()
		self.name = name.lower()
		spec = _importlib.util.spec_from_file_location("main", (path + "/" + mode + "/" + name + "/main.py").replace("//", "/"))
		self.plugin = _importlib.util.module_from_spec(spec)
		spec.loader.exec_module(self.plugin)
		self.info = DroitPluginInfo(mode, name, path=path)
		if(self.mode == "input"):
			if("preloadScript" in self.info.info.keys()):
				_os.system("python3 " + path+"/input/"+name+"/"+self.info.info["preloadScript"])


class DroitPluginInfo:
	"""Contains information about a DroitPlugin"""
	def __init__(self, mode: str, name: str, path=_os.path.dirname(__file__)+"/plugins"):
		self.mode = mode
		self.name = name
		if(mode == "input"):
			self.info = _json.loads(open((path+"/"+mode+"/"+name+"/info.json").replace("//", "/"), "r").read())
			self.description = self.info["description"]
			self.attrib = self.info["attributes"]


class DroitSearchHit:
	"""Object returned by useRules()"""
	def __init__(self, rule: DroitRule, variables: dict, ranking: int):
		self.rule = rule
		self.variables = variables
		self.ranking = ranking


class DroitHistory:
	"""List of inputs and outputs of python-droit."""
	def __init__(self):
		self.inputs = []
		self.outputs = []
		self.rules = []

	def newEntry(self, userinput: DroitUserinput, rule: DroitRule, output: str):
		self.inputs.append(userinput)
		self.rules.append(rule)
		self.outputs.append(output)

	def saveHistory(self, filename: str):
		m = {"inputs": self.inputs, "outputs": self.outputs}
		open(filename, "w").write(_json.dumps(m))
	
	def loadHistory(self, filename: str):
		m = _json.loads(open(filename, "r").read())
		self.inputs = m["inputs"]
		self.outputs = m["outputs"]