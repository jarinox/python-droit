# dumper.py - write a parsed Droit Databases to XML
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def escapeCharacters(string: str) -> str:
	return string.replace("\\", "\\\\").replace(":", "\\:").replace("!", "\\!").replace("->", "-\\>")

def writeScript(dda, filename):
	"""Write a parse Droit Database to a Droit Database Script file"""
	out = writeScriptString(dda)
	open(filename, "w").write(out)

def writeScriptString(dda) -> str:
	"""Write a parse Droit Database to a Droit Database Script string"""
	out = "Created using python-droit and 'writeScript'\n\n"

	for rule in dda:
		for inRule in rule.input:
			out += inRule.tag.upper()

			if(inRule.attrib):
				attribs = list(inRule.attrib.items())
				for attrib in attribs:
					out += "*" + attrib[1]
			out += "!"

			for value in inRule.children:
				if(out[-1] != "!"):
					out += ","
				out += escapeCharacters(value)
			
			out += ":"
		
		out = out[0:-1] + "->"

		for outRule in rule.output:
			out += outRule.tag.upper()
			out += "!"
			
			for value in outRule.children:
				if(out[-1] != "!"):
					out += ","
				out += escapeCharacters(value)
			
			out += ":"
		
		out = out[0:-1] + "\n"
	
	out = out.replace("TEXT*true!", "NOTX!")
	return out
