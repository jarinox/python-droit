# models.py - structure python-droit data
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


import importlib
from droit.io import DroitIO


class DroitResourcePackage:
	def __init__(self, settings=None):
		self.tools = importlib.import_module("droit.tools")
		self.io = DroitIO()
		self.settings = settings
		self.plugins = []


class DroitGmrResource:
	def __init__(self, gmrModule=None, gmrDatabase=None):
		self.gmrModule = gmrModule
		self.gmrDatabase = gmrDatabase


class DroitRuleInOut:
	def __init__(self, tag, attrib, children, mode):
		self.mode = mode
		self.tag = tag
		self.attrib = attrib
		self.children = children


class DroitRule:
	def __init__(self, inputRules, outputRules):
		self.input = inputRules
		self.output = outputRules


class DroitUserinput:
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
	def __init__(self, mode, name):
		self.mode = mode.lower()
		self.name = name.lower()
		self.plugin = importlib.import_module("droit.plugins." + mode + "." + name + ".main")
