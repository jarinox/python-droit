# python-droit - a simple library for creating bots
# Copyright 2020 Jakob Stolze <https://github.com/jarinox>
#
# Version 1.1.0:6 alpha
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

import os as _os
import time as _time
import importlib as _importlib

from . import models
from . import legacy

from . import loader as _loader
from . import dumper as _dumper

__version__ = "1.1.0:6"
__author__ = "Jakob Stolze"



class Database:
    """A Droit Database that can be used to process rules."""
    def __init__(self, multiSession=False):
        self.rules = models.DroitRule(inputRules=[], outputRules=[])
        self.plugins = []
        self.cache = models.DroitCache()
        self.history = models.DroitHistory()
        self.temp = {"plugins": {}}

        if(multiSession):
            self.sessions = models.DroitMultiSession()
        else:
            self.sessions = False

    def parseLegacy(self, filename: str):
        """Legacy parsing algorithm for Droit Database Script (.dda)"""
        self.rules = _loader.parseLegacy(filename, self.plugins)

    def parseScript(self, filename: str, plugins=True, append=False):
        """Parse a Droit Database Script file (.dda)"""
        newRules = []

        if(self.plugins and plugins):
            newRules = _loader.parseScript(filename, plugins=self.plugins)
        else:
            newRules = _loader.parseScript(filename)
        
        if(append):
            for rule in newRules:
                self.rules.append(rule)
        else:
            self.rules = newRules
    
    def parseScriptString(self, text: str, plugins=True, append=False):
        """Parse Droit Database Script from a string"""
        newRules = []

        if(self.plugins and plugins):
            newRules = _loader.parseScriptString(text, plugins=self.plugins)
        else:
            newRules = _loader.parseScriptString(text)
        
        if(append):
            for rule in newRules:
                self.rules.append(rule)
        else:
            self.rules = newRules
    
    def writeScript(self, filename: str):
        """Write a parsed Droit Database to a Droit Database Script file"""
        _dumper.writeScript(self.rules, filename)
    
    def writeScriptString(self):
        """Write a parsed Droit Database to a Droit Database Script string"""
        return _dumper.writeScriptString(self.rules)

    def loadPlugins(self, location=_os.path.dirname(__file__)+"/plugins", append=True):
        """
        Loads all plugins from the given location and returns them in a
        list containing DroitPlugin items.
        """
        if not(append):
            self.plugins = []

        inList = _os.listdir(path=location+"/input")
        outList = _os.listdir(path=location+"/output")
        
        for name in inList:
            if(_os.path.isdir(location+"/input/"+name)):
                self.plugins.append(models.DroitPlugin("input", name, path=location))
        
        for name in outList:
            if(_os.path.isdir(location+"/output/"+name)):
                self.plugins.append(models.DroitPlugin("output", name, path=location))
    

    def createVariables(self, vars={}, userinput=None):
        """
        Create a dict of variables containing all necessary pieces of data
        for formatOut
        """
        variables = {}
        variables["global.time"] = _time.strftime("%H:%M")
        variables["global.date"] = _time.strftime("%d.%m.%Y")
        variables["global.droitname"] = "Droit"
        variables["global.username"] = ""

        if(self.sessions):
            active = self.sessions.getActive()
            if(active):
                variables["global.username"] = active.username

                if(self.sessions.droitname):
                    variables["global.droitname"] = self.sessions.droitname
                else:
                    variables["global.droitname"] = active.droitname
            else:
                if(self.sessions.droitname):
                    variables["global.droitname"] = self.sessions.droitname

        
        if userinput:
            variables["global.userinput"] = userinput.rawInput
        else:
            variables["global.userinput"] = ""
        
        for var in vars:
            variables[var] = vars[var]
            
        return variables
    

    def useRules(self, userinput: models.DroitUserinput):
        """
        Runs every rule onto the userinput.
        Returns all possible DroitRulesOutput sorted by relevance.
        """
        hits = []

        if not(self.plugins):
            print("Warning: no plugins loaded")

        for i in range(0, len(self.rules)): # use all rules
            variables = {}
            ranking = 0
            blocks = []
            ruleOk = True
            for j in range(0, len(self.rules[i].input)):
                if not(self.rules[i].input[j].tag in blocks):
                    blocks.append(self.rules[i].input[j].tag)
            
            for block in blocks:
                plug = None
                for inPlug in self.plugins:
                    if(inPlug.name == block.lower() and inPlug.mode == "input"):
                        plug = inPlug.plugin
                
                if(plug):
                    passRule, newVars, rankMod, self = plug.block(userinput, i, block, self)
                    for var in newVars:
                        variables[var] = newVars[var]
                    if(passRule):
                        ranking = ranking + rankMod
                    else:
                        ruleOk = False
                        break
                else:
                    ruleOk = False
            
            if(ruleOk):
                rankmod = len(self.rules[i].input) * 0.3 + ranking
                hit = models.DroitSearchHit(self.rules[i], variables, rankmod)
                hits.append(hit)

        if(hits != []):
            hits = sorted(hits, key=lambda hit: hit.ranking, reverse=True)
        
        return hits


    def formatOut(self, outputRules: list, variables: dict):
        """Evaluates a DroitRuleOutput"""
        output = ""

        if not(self.plugins):
            print("Warning: no plugins loaded")

        for i in range(0, len(outputRules)):
            if(outputRules[i].tag.upper() == "EVAL"):
                plugin = ""

                for plug in outputRules[i].children:
                    plugin += plug
                plugin = plugin.split(".", 1)
                for var in variables:
                    if("*" + var in plugin[1]):
                        plugin[1] = plugin[1].replace("*" + var, "\"" + variables[var] + "\"")

                if("(" in plugin[1]):
                    plugin.append(plugin[1].split("(")[1][:-1].replace('"', "").replace(", ", ",").split(","))
                    plugin[1] = plugin[1].split("(")[0]

                params = []
                for i in range(0, len(plugin[2])):
                    params.append(plugin[2][i])
                
                plug = None
                for outPlug in self.plugins:
                    if(outPlug.name == "eval."+plugin[0] and outPlug.mode == "output"):
                        plug = outPlug.plugin
                
                if(plug):
                    method = getattr(plug, plugin[1])
                    
                    outadd = ""
                    outadd, self = method(params, self)

                    output += outadd
            
            
            else:
                plug = None
                for plugin in self.plugins:
                    if(plugin.mode == "output" and outputRules[i].tag.lower() == plugin.name.lower()):
                        plug = plugin.plugin
                
                if(plug):
                    outadd = ""
                    outadd, self = plug.block(outputRules[i], variables, self)
                    output += outadd
        
        return output
    

    def simpleIO(self, text: str, history=True):
        userinput = models.DroitUserinput(text)

        hits = self.useRules(userinput)
        if(hits):
            hit = hits[0]

            variables = self.createVariables(vars=hit.variables)
            output = self.formatOut(hit.rule.output, variables)

            if(history):
                if(self.sessions):
                    if(self.sessions.getActive()):
                        self.history.newEntry(userinput, hit.rule, output, userId=self.sessions.getActive().id)
                    else:
                        self.history.newEntry(userinput, hit.rule, output)
                else:
                    self.history.newEntry(userinput, hit.rule, output)
            
            return output
        else:
            return None
