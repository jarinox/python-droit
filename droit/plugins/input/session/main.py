# main.py - plugins.session - SESSION plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)
#
# SESSION*isActive!               is there an active session?
# SESSION*isNotActive!            is there no active session?
# SESSION*isUsername!<username>   = active username?
# SESSION*isId!<id>               = active id?


def block(userinput, iN, name, db):
	passRule = False
	rankMod = 0
	outVars = {}

	inputRules = db.rules[iN].input

	for rule in inputRules:
		if(rule.tag == "SESSION"):
			if(rule.attrib["cmd"] == "isActive"): # isActive
				if(db.sessions):
					if(db.sessions.getActive()):
						passRule = True
			
			if(rule.attrib["cmd"] == "isNotActive"): # isNotActive
				if not(db.sessions):
					passRule = True
				elif not(db.sessions.getActive()):
					passRule = True
			
			if(rule.attrib["cmd"] == "isUsername"): # isUsername
				if(db.sessions):
					if(db.sessions.getActive()):
						if(db.sessions.getActive().username in rule.children):
							passRule = True
			
			if(rule.attrib["cmd"] == "isId"): # isId
				if(db.sessions):
					if(db.sessions.getActive()):
						if(db.sessions.getActive().id in rule.children):
							passRule = True

	return passRule, outVars, rankMod, db