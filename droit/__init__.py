# python-droit - a simple library for creating bots
# Copyright 2020 Jakob Stolze <https://github.com/jarinox>
#
# Version 1.0.1
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import os, importlib

from .loader import *
from .dumper import *
from .tools import *
from .models import *
from .legacy import *


def useRules(rules, userinput, rpack, rback=False):
	"""
	Uses a parsed Droit Database and runs every rule onto the userinput.
	Returns all possible DroitRulesOutput sorted by relevance.
	"""
	hits = []

	for i in range(0, len(rules)): # use all rules
		variables = {}
		ranking = 0
		blocks = []
		ruleOk = True
		for j in range(0, len(rules[i].input)):
			if not(rules[i].input[j].tag in blocks):
				blocks.append(rules[i].input[j].tag)
		
		path = os.path.dirname(__file__)+"/"
		inPlugs = os.listdir(path+"plugins/input")
		for block in blocks:			
			if(block.lower() in inPlugs):				
				plug = None
				useCache = False
				if(rpack != None):
					for inPlug in rpack.plugins:
						if(inPlug.name == block.lower() and inPlug.mode == "input"):
							useCache = True
							plug = inPlug.plugin
				
				if not(useCache):
					spec = importlib.util.spec_from_file_location("main", path + "plugins/input/" + block.lower() + "/main.py")
					plug = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(plug)

				
				passRule, newVars, rankMod, rpack = plug.block(userinput, rules[i].input, block, rpack)
				for var in newVars:
					variables[var] = newVars[var]
				if(passRule):
					ranking = ranking + rankMod
				else:
					ruleOk = False
					break
			else:
				ruleOk = False
		
		if(ruleOk):
			rankmod = len(rules[i].input) * 0.3 + ranking
			hit = models.DroitSearchHit(rules[i], variables, rankmod)
			hits.append(hit)

	if(hits != []):
		hits = sorted(hits, key=lambda hit: hit.ranking, reverse=True)

	if(rback):
		return hits, rpack
	else:
		return hits



def formatOut(outputRules, variables, rpack, rback=False):
	"""Evaluates a DroitRuleOutput"""
	output = ""
	
	for i in range(0, len(outputRules)):
		if("TEXT" == outputRules[i].tag.upper()):
			for text in outputRules[i].children:
				output += text
		
		if("VAR" == outputRules[i].tag.upper()):
			for var in variables:
				if(var in outputRules[i].children):
					output += variables[var]
		
		if("EVAL" == outputRules[i].tag.upper()):
			plugin = ""
			for plug in outputRules[i].children:
				plugin += plug
			plugin = plugin.split(".", 1)
			for var in variables:
				if("*" + var in plugin[1]):
					plugin[1] = plugin[1].replace("*" + var, "\"" + variables[var] + "\"")

			isMethod = False
			if("(" in plugin[1]):
				isMethod = True
				plugin.append(plugin[1].split("(")[1][:-1].replace('"', "").replace(", ", ",").split(","))
				plugin[1] = plugin[1].split("(")[0]

			params = []
			for i in range(0, len(plugin[2])):
				params.append(plugin[2][i])
			
			plug = None
			useCache = False
			if(rpack != None):
				for outPlug in rpack.plugins:
					if(outPlug.name == plugin[0] and outPlug.mode == "output"):
						useCache = True
						plug = outPlug.plugin

			if not(useCache):
				spec = importlib.util.spec_from_file_location("main", os.path.dirname(__file__) + "/plugins/output/" + plugin[0] + "/main.py")
				plug = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(plug)
			
			method = getattr(plug, plugin[1])
			
			if(isMethod):
				if(plugin[1][1] != ""):
					output, rpack = method(params, rpack)
					break
				else:
					output, rpack = method(rpack)
					break				


	if(rback):
		return output, rpack
	else:
		return output



def simpleIO(rawInput, databasePath):
	"""
	Simple function to test a database and to create simple bots.
	The use is restricted and not recommended because no resources
	can be provided. This function is intended to be used for testing.
	Use an own script to create more complex bots.
	"""
	userinput = models.DroitUserinput(rawInput)
	rpack = models.DroitResourcePackage()
	hits = useRules(loader.parseDroitXML(databasePath), userinput, rpack)
	if(len(hits) > 0):
		return formatOut(hits[0].rule.output, tools.createVariables(inpVars=hits[0].variables, userinput=userinput), rpack)
	else:
		return ""

