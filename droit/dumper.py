# dumper.py - write a parsed Droit Databases to XML
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

import xml.etree.cElementTree as _ET
import xml.dom.minidom as _minidom


def writeDroitXML(dda, filename):
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


def prettifyXML(filename):
	dom = _minidom.parse(filename)
	pretty = dom.toprettyxml()
	open(filename, "w").write(pretty)


def writeScript(dda, filename):
	"""Write a parse Droit Database to a Droit Database Script file"""
	out = writeScriptString(dda)
	open(filename, "w").write(out)

def writeScriptString(dda):
	"""Write a parse Droit Database to a Droit Database Script string"""
	out = "Created using python-droit and 'writeLegacy'\n\n"

	for rule in dda:
		for inRule in rule.input:
			out += inRule.tag.upper()

			if(inRule.attrib):
				out += "*" + list(inRule.attrib.items())[0][1]
			out += "!"

			for value in inRule.children:
				if(out[len(out) - 1] != "!"):
					out += ","
				out += value.replace(":", "&dpp;").replace("!", "&arz;")
			
			out += ":"
		
		out = out[0:len(out) - 1] + "->"

		for outRule in rule.output:
			out += outRule.tag.upper()
			out += "!"
			
			for value in outRule.children:
				if(out[len(out) - 1] != "!"):
					out += ","
				out += value.replace(":", "&dpp;").replace("!", "&arz;")
			
			out += ":"
		
		out = out[0:len(out) - 1] + "\n"
	
	out = out.replace("TEXT*true!", "NOTX!")
	return out