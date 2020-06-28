# __init__.py - io - easy printing to multiple outputs
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import importlib, os


class DroitIO:
	"""input and output from and to multiple sources"""

	def __init__(self, mode="console"):
		self.mode = mode
		self.activeModule = importlib.import_module("droit.io." + self.mode)
		self.moduleList = os.listdir(os.path.dirname(__file__))
	
	def activateModule(self, name):
		"""Change the currently active input/output module"""
		if(name in self.moduleList or name + ".py" in self.moduleList):
			self.activeModule = importlib.import_module("droit.io." + name)
			self.mode = name
		
	def output(self, text):
		"""Output text to the user."""
		return self.activeModule.output(text)
	
	def binaryQuestion(self, question):
		"""Ask a yes or no question. True or False will be returned."""
		return self.activeModule.binaryQuestion(question)
	
	def input(self, question):
		"""Get an input from the user."""
		return self.activeModule.getinput(question)
