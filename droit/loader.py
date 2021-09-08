# loader.py - parse Droit Databases
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)



from . import models as _models
from . import legacy as _legacy
from . import analyzer as _analyzer

from typing import List as _List


def nonEscapeSplit(string: str, divider: str) -> list:
	"""Split a string if the divider isn't escaped."""
	if(len(divider) == 1):
		resp = [""]
		if(len(string) > 1):
			if(string[0] == divider):
				resp.append("")
			else:
				resp = [string[0]]
			for i in range(1, len(string)):
				if(string[i] == divider and string[i-1] != "\\"):
					resp.append("")
				else:
					resp[-1] += string[i]
		else:
			resp = [string]
		return resp
	else:
		print("error: python-droit: divider has to be a single character")
		return False


def escapeCharacters(string: str) -> str:
	return string.replace("\\\\", "\\").replace("\\!", "!").replace("\\:", ":").replace("\\-", "-").replace("\\>", ">")


def parseLegacy(filename: str, plugins) -> _List[_models.DroitRule]:
	"""Parse a legacy Droit Database (.dda)"""
	dda = _legacy.parseDDA(filename)
	rules = []
	pinfos = []
	for plugin in plugins:
		pinfos.append(plugin.info)
	for rule in dda:
		inputrules = []
		outputrules = []
		for inrule in rule[0]:
			attr = {}
			inrule[1] = inrule[1].replace("&arz;", "!").replace("&dpp;", ":")
			if("*" in inrule[0]):
				for info in pinfos:
					if(info.name.lower() == inrule[0].split("*")[0].lower()):
						ipkey = list(info.attrib.keys())[0]
						attr[ipkey] = inrule[0].split("*")[1]
				inrule[0] = inrule[0].split("*")[0]

			if("NOTX" == inrule[0]):
				inrule[0] = "TEXT"
				attr["not"] = "true"
			children = inrule[1].split(",")
			if(inrule[1] == ""):
				children = []
			dri = _models.DroitRuleInput(inrule[0], attr, children)
			inputrules.append(dri)
		for outrule in rule[1]:
			outrule[1] = outrule[1].replace("&arz;", "!").replace("&dpp;", ":")
			if(outrule[0].upper() == "EVAL"):
				dro = _models.DroitRuleOutput(outrule[0].upper(), [outrule[1]])
			else:
				children = outrule[1].split(",")
				if(outrule[1] == ""):
					children = []
				dro = _models.DroitRuleOutput(outrule[0].upper(), children)
			outputrules.append(dro)
		dr = _models.DroitRule(inputrules, outputrules)
		rules.append(dr)
	return rules
		

def parseScript(filename: str, plugins=False, legacyValid=False, warnings=True) -> _List[_models.DroitRule]:
	plain = open(filename, "r").read()
	return parseScriptString(plain, plugins=plugins, legacyValid=legacyValid, warnings=warnings)

def parseScriptString(string: str, plugins=False, legacyValid=False, warnings=True) -> _List[_models.DroitRule]:
	plain = string.split("\n")
	rules = []
	info = ""
	
	lnum = 0
	for line in plain:
		lnum += 1
		if(legacyValid):
			isValid = _legacy.isValidLine(line)
		else:
			isValid, info = _analyzer.isValidLine(line, infos=True)
		
		if(isValid):
			rule = _models.DroitRule([], [])
			inp, out = line.split("->")

			inp = nonEscapeSplit(inp, ":")
			out = nonEscapeSplit(out, ":")

			for inpx in inp:
				inpx = nonEscapeSplit(inpx, "!")
				inpx[0] = inpx[0].replace("NOTX", "TEXT*true")
				
				if(inpx[1] != ""):
					children = escapeCharacters(inpx[1]).split(",")
				else:
					children = []

				if("*" in inpx[0]):
					attr = {}
					parts = inpx[0].split("*")
					block = parts[0].upper()

					if(plugins):
						for plugin in plugins:
							if(plugin.mode == "input" and plugin.name.upper() == block):
								keys = list(plugin.info.attrib.keys())
								if(len(parts) - 1 <= len(keys)):
									for i in range(0, len(parts)-1):
										attr[keys[i]] = parts[i+1]
								else:
									print("warning: python-droit: plugin '" + block + "' takes a maximum of " + str(len(keys)) + " parameters, " + str(len(parts)-1) + " given.")
					else:
						if(block == "INP"):
							attr["var"] = parts[1]
						elif(block == "SIMT"):
							attr["limit"] = parts[1]
						elif(block == "TEXT"):
							attr["not"] = parts[1]
						elif(block == "SESSION"):
							attr["cmd"] = parts[1]
					
					rule.input.append(_models.DroitRuleInput(block, attr, children))
				else:
					rule.input.append(_models.DroitRuleInput(inpx[0], {}, children))
			
			for outx in out:
				outx = nonEscapeSplit(outx, "!")
				if(outx[1] != ""):
					if(outx[0].upper() == "EVAL"):
						children = [escapeCharacters(outx[1])]
					else:
						children = escapeCharacters(outx[1]).split(",")
				else:
					children = []
				rule.output.append(_models.DroitRuleOutput(outx[0], children))

			rules.append(rule)	
		
		elif(info != "comment" and warnings and not(legacyValid)):
			print("warning: python-droit: parseScript: " + info + " [" + str(lnum) + "]")
	return rules