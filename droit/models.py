# models.py - structure python-droit data
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os as _os
import importlib as _importlib
import json as _json
import random as _random



class DroitSession:
	def __init__(self, username: str, droitname=False, ident=_random.randint(0, 100000000000000)):
		self.username = username
		self.droitname = droitname
		self.userData = {}
		self.id = ident

	def fromDict(self, var: dict):
		self.id = var["id"]
		self.username = var["username"]
		self.droitname = var["droitname"]
		self.userData = var["userData"]
	
	def toDict(self) -> dict:
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
				return True
		return False
	
	def activateById(self, ident):
		for i in range(0, len(self.sessions)):
			if(self.sessions[i].id == ident):
				self.active = i
				return True
		return False
	
	def getActive(self) -> DroitSession:
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
	
	def run(self, function, *args, **kargs):
		name = function.__module__ +  "." + function.__name__

		params = [args, kargs]

		for item in self.storage:
			if(item["name"] == name and item["params"] == params):
				return item["value"]
		
		value = function(*args, **kargs)
		
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
		self.mode = "output"
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
		valchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZäöüÄÖÜ1234567890ß "
		for char in rawInput: # remove unnecessary characters
			if(char in valchars):
				pin += char

		while("  " in pin):
			pin = pin.replace("  ", " ") # double blank to single blank
		
		pin = pin.rstrip()
		self.caseInput = pin
		self.simpleInput = pin.lower()
		self.words = self.simpleInput.split(" ") # split up words at blank


class DroitPlugin:
	"""Loads a plugin."""
	def __init__(self, mode: str, name: str, path=_os.path.join(_os.path.dirname(__file__), "plugins"), preloadScript=True):
		self.mode = mode.lower()
		self.name = name.lower()
		spec = _importlib.util.spec_from_file_location("main", _os.path.join(path, mode, name, "main.py"))
		self.plugin = _importlib.util.module_from_spec(spec)
		spec.loader.exec_module(self.plugin)
		self.info = DroitPluginInfo(mode, name, path=path)
		if(self.mode == "input"):
			if("preloadScript" in self.info.info.keys() and preloadScript):
				_os.system("python3 " + _os.path.join(path, "input", name, self.info.info["preloadScript"]))


class DroitPluginInfo:
	"""Contains information about a DroitPlugin"""
	def __init__(self, mode: str, name: str, path=_os.path.join(_os.path.dirname(__file__), "plugins")):
		self.mode = mode
		self.name = name
		if(mode == "input"):
			self.info = _json.loads(open(_os.path.join(path, mode, name, "info.json"), "r").read())
			self.description = self.info["description"]
			self.attrib = self.info["attributes"]
			files = _os.listdir(_os.path.join(path, mode, name))
			self.req = ("req.py" in files)


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


class DroitDatabaseInfo:
	"Information about a Droit Datbase"
	def __init__(self, author=None, license=None, ddsVersion=None, attrib={}):
		if(author):
			self.author = [author]
		else:
			self.author = []
		
		if(ddsVersion):
			self.ddsVersion = [ddsVersion]
		else:
			self.ddsVersion = []

		if(license):
			self.license = [license]
		else:
			self.license = []

		self.attrib = attrib


	def add(self, attribs):
		for key in attribs:
			lkey = key.lower()
			if(lkey == "author"):
				if not(attribs[key] in self.author):
					self.author.append(attribs[key])	
			elif(lkey =="license" or lkey == "licence"):
				if(not license in self.license):
					self.license.append(attribs[key])		
			elif(lkey == "dds" or lkey == "ddsversion"):
				if not(attribs[key] in self.ddsVersion):
					self.ddsVersion.append(attribs[key])
			else:
				self.attrib[lkey] = attribs[key]