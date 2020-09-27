# models.py - structure python-droit data
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os as _os
import importlib as _importlib
import json as _json
import random as _random



class DroitSession:
	def __init__(self, username, droitname=False, ident=_random.randint(0, 100000000000000)):
		self.username = username
		self.droitname = droitname
		self.userData = {}
		self.id = ident

	def fromDict(self, var):
		self.id = var["id"]
		self.username = var["username"]
		self.droitname = var["droitname"]
		self.userData = var["userData"]
	
	def toDict(self):
		return {
			"id": self.id,
			"username": self.username,
			"droitname": self.droitname,
			"userData": self.userData
		}

class DroitMultiSession:
	def __init__(self, path=None, droitname=False):
		self.sessions = []
		self.active = -1
		self.path = None
		self.droitname=droitname
	
	def activateByUsername(self, username):
		for i in range(0, len(self.sessions)):
			if(self.sessions[i].username == username):
				self.active = i
				break
	
	def activateById(self, ident):
		for i in range(0, len(self.sessions)):
			if(self.sessions[i].id == ident):
				self.active = i
				break
	
	def getActive(self):
		if(self.active != -1 and self.active < len(self.sessions)):
			return self.sessions[self.active]
		else:
			return False
	
	def setActive(self, session):
		if(self.active != -1 and self.active < len(self.sessions)):
			self.sessions[self.active] = session
	
	def loadSessions(self, append=False):
		if not(append):
			self.sessions = []
		
		with open(self.path, "r") as f:
			data = _json.load(f)
			self.droitname = data["droitname"]
			self.active = data["active"]

			sessions = data["sessions"]
			for session in sessions:
				s = DroitSession("")
				s.fromDict(session)
				self.sessions.append(s)

	def saveSessions(self):
		dump = []
		for session in self.sessions:
			dump.append(session.toDict())
		
		with open(self.path, "w") as f:
			_json.dump({"sessions": dump, "droitname": self.droitname, "active": self.active}, f)

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
		pin = ""
		valchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöüÄÖÜ1234567890 "
		for char in rawInput: # remove unnecessary characters
			if(char in valchars):
				pin += char

		while("  " in pin):
			pin = pin.replace("  ", " ") # double blank to single blank
		
		pin = pin.rstrip()
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
		self.userIds = []

	def newEntry(self, userinput: DroitUserinput, rule: DroitRule, output: str, userId=False):
		self.inputs.append(userinput)
		self.rules.append(rule)
		self.outputs.append(output)
		self.userIds.append(userId)