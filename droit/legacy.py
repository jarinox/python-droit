# legacy.py - parse legacy (v0.4) Droit Databases
# Copyright 2019 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


import xml.etree.cElementTree as _ET
import xml.dom.minidom as _minidom

from . import models as _models


def isValidLine(ddaFileLine: str) -> bool:
	"""Checks whether a Droit Database rule is valid or e.g. a comment."""
	ddaFileLine = ddaFileLine.replace("\\:", "").replace("\\!", "").replace("\\>", "")
	valid = True
	if not("->" in ddaFileLine) or (len(ddaFileLine.split("->")) != 2):
		valid = False
	if valid:
		if(ddaFileLine.split("->")[0] == "" or ddaFileLine.split("->")[1] == ""):
			valid = False
	if valid:
		lin = ddaFileLine.split("->")[0].split(":")
		for i in range(0, len(lin)):
			if(len(lin[i].split("!")) != 2):
				valid = False
	if valid:
		lout = ddaFileLine.split("->")[1].split(":")
		for i in range(0, len(lout)):
			if(len(lout[i].split("!")) != 2):
				valid = False
	return valid


def parseDDA(filename: str) -> list:
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


def parseDroitXML(filename: str):
	"""Parse a Droit XML Database"""
	tree = _ET.parse(filename)
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
								dri = _models.DroitRuleInput(inrule.tag.upper(), inrule.attrib, children)
								inputrules.append(dri)
					for outrules in rule:
						if(outrules.tag == "output"):
							for outrule in outrules:
								children = []
								for outchild in outrule:
									if(outchild.text != None):
										children.append(outchild.text)
								dro = _models.DroitRuleOutput(outrule.tag.upper(), children)
								outputrules.append(dro)
					dr = _models.DroitRule(inputrules, outputrules)
					rules.append(dr)
	return rules


def writeDroitXML(dda, filename: str):
	"""Write a parse Droit Database to XML"""
	droitdb = _ET.Element("droitdb")
	droitxml = _ET.SubElement(droitdb, "droitxml")
	
	for rule in dda:
		r = _ET.SubElement(droitxml, "rule")
		inp = _ET.SubElement(r, "input")
		out = _ET.SubElement(r, "output")
		for inRule in rule.input:
			sub = _ET.SubElement(inp, inRule.tag, attrib=inRule.attrib)
			for child in inRule.children:
				_ET.SubElement(sub, "item").text = child
		for outRule in rule.output:
			sub = _ET.SubElement(out, outRule.tag)
			for child in outRule.children:
				_ET.SubElement(sub, "item").text = child
		
	
	tree = _ET.ElementTree(droitdb)
	tree.write(filename)


def prettifyXML(filename: str):
	dom = _minidom.parse(filename)
	pretty = dom.toprettyxml()
	open(filename, "w").write(pretty)