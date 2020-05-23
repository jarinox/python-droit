# dumper.py - write a parsed Droit Databases to XML
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)

import xml.etree.cElementTree as ET
import xml.dom.minidom


def writeDroitXML(dda, filename):
	"""Write a parse Droit Database to XML"""
	droitdb = ET.Element("droitdb")
	droitxml = ET.SubElement(droitdb, "droitxml")
	
	for rule in dda:
		r = ET.SubElement(droitxml, "rule")
		inp = ET.SubElement(r, "input")
		out = ET.SubElement(r, "output")
		for inRule in rule.input:
			sub = ET.SubElement(inp, inRule.tag, attrib=inRule.attrib)
			for child in inRule.children:
				ET.SubElement(sub, "item").text = child
		for outRule in rule.output:
			sub = ET.SubElement(out, outRule.tag, attrib=outRule.attrib)
			for child in outRule.children:
				ET.SubElement(sub, "item").text = child
		
	
	tree = ET.ElementTree(droitdb)
	tree.write(filename)


def prettifyXML(filename):
	dom = xml.dom.minidom.parse(filename)
	pretty = dom.toprettyxml()
	open(filename, "w").write(pretty)
