# loader.py - parse Droit Databases
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import xml.etree.cElementTree as ET
from droit import models, legacy, tools



def parseDroitXML(filename):
	"""Parse a Droit XML Database"""
	tree = ET.parse(filename)
	root = tree.getroot()
	rules = []
	for child in root:
		if(child.tag == "droitxml"):
			for rule in child:
				if(rule.tag == "rule"):
					inputrules = []
					outputrules = []
					for inrules in rule:
						if(inrules.tag == "input"):
							for inrule in inrules:
								children = []
								for inchild in inrule:
									if(inchild.text != None):
										children.append(inchild.text)
								dri = models.DroitRuleInOut(inrule.tag.upper(), inrule.attrib, children, "input")
								inputrules.append(dri)
					for outrules in rule:
						if(outrules.tag == "output"):
							for outrule in outrules:
								children = []
								for outchild in outrule:
									if(outchild.text != None):
										children.append(outchild.text)
								dro = models.DroitRuleInOut(outrule.tag.upper(), outrule.attrib, children, "output")
								outputrules.append(dro)
					dr = models.DroitRule(inputrules, outputrules)
					rules.append(dr)
	return rules


def parseLegacy(filename):
	"""Parse a legacy Droit Database (.dda)"""
	dda = legacy.parseDDA(filename)
	rules = []
	pinfos = tools.loadPluginInfos()
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
			dri = models.DroitRuleInOut(inrule[0], attr, children, "input")
			inputrules.append(dri)
		for outrule in rule[1]:
			attr = {}
			outrule[1] = outrule[1].replace("&arz;", "!").replace("&dpp;", ":")
			if(outrule[0].upper() == "EVAL"):
				dro = models.DroitRuleInOut(outrule[0].upper(), attr, [outrule[1]], "output")
			else:
				children = outrule[1].split(",")
				if(outrule[1] == ""):
					children = []
				dro = models.DroitRuleInOut(outrule[0].upper(), attr, children, "output")
			outputrules.append(dro)
		dr = models.DroitRule(inputrules, outputrules)
		rules.append(dr)
	return rules
		
