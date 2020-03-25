# core.py
# droit core for python
# Copyright 2019 Jakob Stolze
#
# Version              v0.4.1.2
# Date last modified   30.11.2019
# Date created         08.05.2019
# Python Version       3.x
#
# DDS Version          v0.5
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
# der GNU General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
# veröffentlichten Version, weiter verteilen und/oder modifizieren.

# Dieses Programm wird in der Hoffnung bereitgestellt, dass es nützlich sein wird, jedoch
# OHNE JEDE GEWÄHR,; sogar ohne die implizite
# Gewähr der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
# Siehe die GNU General Public License für weitere Einzelheiten.

# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <https://www.gnu.org/licenses/>.


import time, importlib, os, json


class ResourcePackage:
	"""
	Object used to provide resources like the grammar database
	from the main script to the plugins.
	"""
	def __init__(self, gmrModule=None, gmrDatabase=None):
		self.gmrModule = gmrModule
		self.gmrDatabase = gmrDatabase


def isValidLine(ddaFileLine):
	"""Checks wether a Droit Database rule is valid or e.g. a comment."""
	valid = True
	if not("->" in ddaFileLine) or (len(ddaFileLine.split("->")) != 2):
		valid = False
	if valid:
		if(ddaFileLine.split("->")[0] == "" or ddaFileLine.split("->")[1] == ""):
			valid = False
	if valid:
		lin = ddaFileLine.split("->")[0].split(":")
		for i in range(0, len(lin)):
			block = lin[i].split("!")[0]
			if("*" in block):
				block = block.split("*")[0]
			if(len(lin[i].split("!")) != 2):
				valid = False
	if valid:
		lout = ddaFileLine.split("->")[1].split(":")
		for i in range(0, len(lout)):
			block = lout[i].split("!")[0]
			if(len(lout[i].split("!")) != 2):
				valid = False
	return valid

def parseDDA(filename, mode="strict"):
	"""Parse a Droit Database (.dda) file."""
	ddaFile = open(filename, "r").read().split("\n")
	ddaData = []
	for i in range(0, len(ddaFile)):
		if(mode == "fast"): # fast import (may cause errors due to defective DDS)
			if("->" in ddaFile[i]):
				ddaData.append(ddaFile[i].split("->"))
		if(mode == "strict"): # strict check on accuracy of imported lines (recommended)
			if(isValidLine(ddaFile[i])):
				ddaData.append(ddaFile[i].split("->"))

	
	for i in range(0, len(ddaData)):
		ddaData[i][0] = ddaData[i][0].split(":")
		ddaData[i][1] = ddaData[i][1].split(":")
		for j in range(0, len(ddaData[i][0])):
			ddaData[i][0][j] = ddaData[i][0][j].split("!")
		for j in range(0, len(ddaData[i][1])):
			ddaData[i][1][j] = ddaData[i][1][j].split("!")

	return ddaData


def prepareInput(userinput):
	"""
	Removes unnecessary characters and splits the words at blanks.
	Returns a list.
	"""
	rmchars = [",", ":", "!", ".", "-", "?", ";", "'", "\"", "(", ")", "$"]
	for i in range(0, len(rmchars)): # remove unnecessary characters
		userinput = userinput.replace(rmchars[i], "")
	userinput = userinput.replace("  ", " ") # double blank to single blank
	userinput = userinput.split(" ") # split up words at blank
	return userinput


def useRules(rules, userinput, rpack=None):
	"""
	Uses a parsed Droit Database and runs every rule onto the userinput.
	Returns all possible rules sorted by relevance.
	"""
	hits = []
	uip = userinput[0]
	for i in range(1, len(userinput)):
		uip = uip + " " + userinput[i]
	
	for i in range(0, len(rules)): # use all rules
		rcount = 0
		ranking = 0
		variables = []
		srtx = False
		for j in range(0, len(rules[i][0])): # use every element of the rule
			for k in range(0, len(userinput)): # user every word of the userinput
				
				if("TEXT" == rules[i][0][j][0]):
					if(userinput[k].lower() in rules[i][0][j][1].split(",")):
						rcount += 1
				
				elif("NOTX" == rules[i][0][j][0]):
					notx = True
					for l in range(0, len(userinput)):
						if(userinput[l].lower() in rules[i][0][j][1].split(",")):
							notx = False
					if(notx):
						rcount += 1
					ranking += 1
					break
				
				elif("SRTX" == rules[i][0][j][0]):
					if(uip.lower() in rules[i][0][j][1].split(",")):
						rcount = len(rules[i][0])
						srtx = True
				
				elif("INP" == rules[i][0][j][0].split("*")[0]):
					if(len(userinput) > j and k == j):
						if(rules[i][0][j][1] == "" or userinput[k] in rules[i][0][j][1].split(",")):
							variables.append([rules[i][0][j][0].split("*")[1], userinput[k]])
							rcount += 1
							ranking += 1
				
				elif("INP2" == rules[i][0][j][0].split("*")[0]):
					if(len(userinput) > j and k == j):
						varadd = userinput[k]
						for l in range(1, len(userinput) - k):
							varadd = varadd + " " + userinput[k + l]
						if(rules[i][0][j][1] == "" or varadd in rules[i][0][j][1].split(",")):
							variables.append([rules[i][0][j][0].split("*")[1], varadd])
							rcount += 1
							ranking += 1
				
				elif(rules[i][0][j][0].lower() in os.listdir("plugins/input")):
					p = importlib.import_module("plugins.input." + rules[i][0][j][0].lower() + ".main")
					pback = p.block(userinput, k, rules[i][0][j][1], rpack)
					if(pback[0]):
						if(p.rcountAdd):
							rcount += 1
						if(p.rcountIs):
							rcount = p.rcountIsValue
						if(p.ranking):
							ranking += 1
						if(p.var):
							for l in range(0, len(pback[1])):
								variables.append(pback[1][l])
						if(p.brk):
							break
					
		
		if(rcount == len(rules[i][0])):
			if(srtx):
				rcount = len(userinput)
			hits.append([rules[i][1], variables, len(userinput) - rcount + ranking])
	
	if(hits != []):
		hits = sorted(hits, key=lambda hit: hit[2])
	return hits


def createVariables(inpVars=[], username="unknown", droitname="Droit", userinput=""):
	"""
	Create a list of variables containing all necessary pieces of data
	for formatOut and runOutputPlugin.
	"""
	variables = []
	variables.append(["global.time", time.strftime("%H:%M")])
	variables.append(["global.date", time.strftime("%d.%m.%Y")])
	variables.append(["global.username", username])
	variables.append(["global.droitname", droitname])
	variables.append(["global.userinput", userinput])
	for i in range(0, len(inpVars)):
		variables.append(["inp." + inpVars[i][0], inpVars[i][1]])
	return variables


def runOutputPlugin(plugin, variables, rpack=None):
	"""Evaluates a plugin."""
	plugin = plugin.split(".", 1)
	for i in range(0, len(variables)):
		if("*" + variables[i][0] in plugin[1]):
			plugin[1] = plugin[1].replace("*" + variables[i][0], "\"" + variables[i][1] + "\"")
	
	isMethod = False
	if("(" in plugin[1]):
		isMethod = True
		plugin.append(plugin[1].split("(")[1][:-1].replace('"', ""))
		plugin[1] = plugin[1].split("(")[0]
	
	params = []
	for i in range(2, len(plugin)):
		params.append(plugin[i])
	
	plug = importlib.import_module("plugins.output." + plugin[0] + ".main")
	method = getattr(plug, plugin[1])
	
	if(isMethod):
		if(plugin[1][1] != ""):
			return method(params, rpack)
		else:
			return method(rpack)
	else:
		return methodW


def formatOut(outRules, variables, rpack=None):
	"""Evaluates a Droit Database rule."""
	output = ""
	for i in range(0, len(outRules)):
		
		if("TEXT" == outRules[i][0]):
			output += outRules[i][1]
		
		if("VAR" == outRules[i][0]):
			for j in range(0, len(variables)):
				if(variables[j][0] == outRules[i][1]):
					output += variables[j][1]
				
		if("EVAL" == outRules[i][0]):
			output += runOutputPlugin(outRules[i][1], variables, rpack=rpack)
	
	output = output.replace("&arz;", "!").replace("&dpp;", ":")
	return output


def simpleIO(userinput, databasePath):
	"""
	Simple function to test a database and to create simple bots.
	The use is restricted and not recommended because no resources
	can be provided.
	Use an own script to create more complex bots.
	"""
	x = useRules(parseDDA(databasePath), prepareInput(userinput))
	if(x != []):
		return formatOut(x[0][0], createVariables(inpVars=x[0][1], userinput=userinput))
	else:
		return ""


