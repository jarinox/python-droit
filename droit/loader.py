# loader.py - parse Droit Databases
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)



from . import models as _models
from . import legacy as _legacy

from typing import List as _List


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
		

def parseScript(filename: str, plugins=False) -> _List[_models.DroitRule]:
	plain = open(filename, "r").read()
	return parseScriptString(plain, plugins=plugins)

def parseScriptString(string: str, plugins=False) -> _List[_models.DroitRule]:
	plain = string.split("\n")
	rules = []
	
	for line in plain:
		if(_legacy.isValidLine(line)):
			rule = _models.DroitRule([], [])
			inp, out = line.split("->")

			inp = inp.split(":")
			out = out.split(":")

			for inpx in inp:
				inpx = inpx.split("!")
				inpx[0] = inpx[0].replace("NOTX", "TEXT*true")
				
				if(inpx[1] != ""):
					children = inpx[1].replace("&arz;", "!").replace("&dpp;", ":").split(",")
				else:
					children = []

				if("*" in inpx[0]):
					attr = {}
					block, atnm = inpx[0].split("*")
					block = block.upper()

					if(plugins):
						for plugin in plugins:
							if(plugin.mode == "input" and plugin.name.upper() == block):
								attr[list(plugin.info.attrib.keys())[0]] = atnm
					else:
						if(block == "INP"):
							attr["var"] = atnm
						elif(block == "SIMT"):
							attr["limit"] = atnm
						elif(block == "TEXT"):
							attr["not"] = atnm
						elif(block == "SESSION"):
							attr["cmd"] = atnm
					
					rule.input.append(_models.DroitRuleInput(block, attr, children))
				else:
					rule.input.append(_models.DroitRuleInput(inpx[0], {}, children))
			
			for outx in out:
				outx = outx.split("!")
				if(outx[1] != ""):
					if(outx[0].upper() == "EVAL"):
						children = [outx[1].replace("&arz;", "!").replace("&dpp;", ":")]
					else:
						children = outx[1].replace("&arz;", "!").replace("&dpp;", ":").split(",")
				else:
					children = []
				rule.output.append(_models.DroitRuleOutput(outx[0], children))

			rules.append(rule)	

	return rules


def parseScriptInfoString(string: str) -> dict:
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