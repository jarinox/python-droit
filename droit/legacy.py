# legacy.py - parse legacy (v0.4) Droit Databases
# Copyright 2019 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def isValidLine(ddaFileLine):
	"""Checks whether a Droit Database rule is valid or e.g. a comment."""
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


def parseDDA(filename):
	"""Parses a Droit Database Script file to the legacy list standard"""
	ddaFile = open(filename, "r").read().split("\n")
	ddaData = []
	for i in range(0, len(ddaFile)):
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
