# core.py
# droit core for python
#
# Author               Jakob Stolze
# Version              v0.4.0.2
# Date last modified   13.06.2019
# Date created         08.05.2019
# Python Version       3.x
#
# DDS Version          v0.4
#
# Copyright 2019 Jakob Stolze 


import time, importlib, os



def isValidLine(ddaFileLine):
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
	rmchars = [",", ":", "!", ".", "-", "?", ";", "'", "\"", "(", ")", "$"]
	for i in range(0, len(rmchars)): # remove unnecessary characters
		userinput = userinput.replace(rmchars[i], "")
	userinput = userinput.replace("  ", " ") # double blank to single blank
	userinput = userinput.lower() # characters to lower
	userinput = userinput.split(" ") # split up words at blank
	return userinput


def useRules(rules, userinput):
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
					if(userinput[k] in rules[i][0][j][1].split(",")):
						rcount += 1
				
				elif("NOTX" == rules[i][0][j][0]):
					notx = True
					for l in range(0, len(userinput)):
						if(userinput[l] in rules[i][0][j][1].split(",")):
							notx = False
					if(notx):
						rcount += 1
					ranking += 1
					break
				
				elif("SRTX" == rules[i][0][j][0]):
					if(uip in rules[i][0][j][1].split(",")):
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
					pback = p.block(userinput, k, rules[i][0][j][1])
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
	variables = []
	variables.append(["global.time", time.strftime("%H:%M")])
	variables.append(["global.date", time.strftime("%d.%m.%Y")])
	variables.append(["global.username", username])
	variables.append(["global.droitname", droitname])
	variables.append(["global.userinput", userinput])
	for i in range(0, len(inpVars)):
		variables.append(["inp." + inpVars[i][0], inpVars[i][1]])
	return variables


def runOutputPlugin(plugin, variables):
	plugin = plugin.split(".", 1)
	for i in range(0, len(variables)):
		if("*" + variables[i][0] in plugin[1]):
			plugin[1] = plugin[1].replace("*" + variables[i][0], "\"" + variables[i][1] + "\"")
	
	# ~ isMethod = False
	# ~ if("(" in plugin[1]):
		# ~ isMethod = True
		# ~ plugin.append(plugin[1].split("(")[1][:-1].replace('"', ""))
		# ~ plugin[1] = plugin[1].split("(")[0]
	
	# ~ plug = importlib.import_module("plugins.output." + plugin[0] + ".main")
	# ~ method = getattr(plug, plugin[1])
	# ~ if(isMethod):
		# ~ if(plugin[1][1] != ""):
			# ~ return method(plugin[2])
		# ~ else:
			# ~ return method()
	# ~ else:
		# ~ return method
	
	# --------------------------------------------------------------------
	# This is just a temporal work-around for the outcommented script above
	# The current problem is to pass multiple arguments from a string to the method
	
	open("plug.py", "w").write("from plugins.output." + plugin[0] + " import main as " + plugin[0] + "\ndef main():\n    return " + plugin[0] + "." + plugin[1])
	import plug
	return plug.main()
	
	# --------------------------------------------------------------------


def formatOut(outRules, variables):
	output = ""
	for i in range(0, len(outRules)):
		
		if("TEXT" == outRules[i][0]):
			output += outRules[i][1]
		
		if("VAR" == outRules[i][0]):
			for j in range(0, len(variables)):
				if(variables[j][0] == outRules[i][1]):
					output += variables[j][1]
				
		if("EVAL" == outRules[i][0]):
			output += runOutputPlugin(outRules[i][1], variables)
	
	output = output.replace("&arz;", "!").replace("&dpp;", ":")
	return output


def simpleIO(userinput, databasePath):
	x = useRules(parseDDA(databasePath), prepareInput(userinput))
	if(x != []):
		return formatOut(x[0][0], createVariables(inpVars=x[0][1], userinput=userinput))
	else:
		return ""

# print(simpleIO("wie geht es dir", "main.dda"))
# print(parseDDA("main.dda"))
