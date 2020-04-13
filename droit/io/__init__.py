# __init__.py - io - easy printing to multiple outputs
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)


from droit.tools import SettingsObject


class DroitIO:
	def __init__(self):
		self.mode = SettingsObject().settings["ioMode"]
		self.activeModule = importlib.import_module("droit.io." + self.mode)
		self.moduleList = os.listdir("droit/io/")
	
	def activateModule(self, name):
		if(name in self.moduleList):
			self.activeModule = importlib.import_module("droit.io." + name)
			self.mode = name
		
	def output(self, text):
		return self.activeModule.output(text)
	
	def binaryQuestion(self, question):
		return self.activeModule.binaryQuestion(question)
	
	def input(self, question):
		return self.activeModule.input(question)