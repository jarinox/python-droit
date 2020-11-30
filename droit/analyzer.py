# analyzer.py - analyze and fix Droit Datbase Scripts
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def parseScriptInfoString(string: str) -> dict:
	"""Parse Droit Database Metadata"""
	data = string.split("\n")
	ret = {}
	for line in data:
		if(len(line) > 3):
			if(line[0] == "@" and " " in line):
				parts = line.split(" ")
				if(len(parts) > 0):
					if(" ".join(parts[1:]).replace(" ", "") != ""):
						ret[parts[0][1:]] = " ".join(parts[1:])
	
	return ret


def upgradeScript(script: str) -> str:
	"""Migrate a Droit Datbase Script to the latest version of Droit Database Script"""
	info = parseScriptInfoString(script)
	if("dds" in info.keys()):
		if(info["dds"] == "1.1"):
			script = script.replace("\\", "\\\\").replace("&arz;", "\\!").replace("&dpp;", "\\:")
	elif("&arz;" in script or "&dpp;" in script):
		script = script.replace("\\", "\\\\").replace("&arz;", "\\!").replace("&dpp;", "\\:")
	return script


def isValidLine(string: str, infos=False) -> bool:
	"""Advanced function to check whether a line is valid or e.g. a comment"""
	valid = True
	info = "valid"
	string = string.replace("\\:", "").replace("\\!", "").replace("\\>", "")

	if not("->" in string):
		valid = False
		info = "comment"
	elif(len(string.split("->")) != 2):
		valid = False
		if(infos):
			info = "The '->' seperator is used more than one time within this line."
	else:
		inp, out = string.split("->")
		if(inp == "" or out == ""):
			valid = False
			if(infos):
				info = "Empty input or output rule."
		else:
			inParts = inp.split(":")
			for i in range(0, len(inParts)):
				inParts[i] = inParts[i].split("!")
				if(len(inParts[i]) != 2):
					valid = False
					if(infos):
						info = "Invalid condition: " + "!".join(inParts[i])
				elif(inParts[i][0] == ""):
					valid = False
					if(infos):
						info = "Empty command name: " + "!".join(inParts[i])
				elif("*" in inParts[i][0]):
					if(inParts[i][0].split("*")[0] == ""):
						valid = False
						if(infos):
							info = "Empty command name: " + "!".join(inParts[i])

			outParts = out.split(":")
			for i in range(0, len(outParts)):
				outParts[i] = outParts[i].split("!")
				if(len(outParts[i]) != 2):
					valid = False
					if(infos):
						info = "Invalid command: " + "!".join(outParts[i])
				elif(outParts[i][0] == ""):
					valid = False
					if(infos):
						info = "Empty command name: " + "!".join(outParts[i])

	if(infos):
		return valid, info
	else:
		return valid