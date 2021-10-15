# python-droit - a simple library for creating bots
# Copyright 2020-2021 Jakob Stolze <https://github.com/jarinox> 
# Email: c4ehhehfa@relay.firefox.com
#
# Version 1.1.2
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
import inspect as _inspect

from . import models
from . import legacy
from . import analyzer

from . import loader as _loader
from . import dumper as _dumper

from typing import List as _List

__version__ = "1.1.2"
__author__ = "Jakob Stolze"



class Database:
    """A Droit Database that can be used to process rules."""
    def __init__(self, multiSession=False):
        self.rules = []
        self.info = models.DroitDatabaseInfo()
        self.plugins = []
        self.pluginReq = {}
        self.cache = models.DroitCache()
        self.history = models.DroitHistory()
        self.temp = {"plugins": {}}
        self.input = input
        self.output = print

        if(multiSession):
            self.sessions = models.DroitMultiSession()
        else:
            self.sessions = False

    def parseLegacy(self, filename: str):
        """Legacy parsing algorithm for Droit Database Script (.dda)"""
        self.rules = _loader.parseLegacy(filename, self.plugins)

    def parseScript(self, filename: str, plugins=True, append=False, legacyValid=False, warnings=True):
        """Parse a Droit Database Script file (.dda)"""
        newRules = []

        string = open(filename, "r").read()

        if(self.plugins and plugins):
            newRules = _loader.parseScriptString(string, plugins=self.plugins, legacyValid=legacyValid, warnings=warnings)
        else:
            newRules = _loader.parseScriptString(string, legacyValid=legacyValid, warnings=warnings)

        infos = analyzer.parseScriptInfoString(string)
        self.info.add(infos)
        
        if(append):
            for rule in newRules:
                self.rules.append(rule)
        else:
            self.rules = newRules
    
    def parseScriptString(self, text: str, plugins=True, append=False, legacyValid=False, warnings=True):
        """Parse Droit Database Script from a string"""
        newRules = []

        if(self.plugins and plugins):
            newRules = _loader.parseScriptString(text, plugins=self.plugins, legacyValid=legacyValid, warnings=warnings)
        else:
            newRules = _loader.parseScriptString(text, legacyValid=legacyValid, warnings=warnings)
        
        infos = analyzer.parseScriptInfoString(text)
        self.info.add(infos)
        
        if(append):
            for rule in newRules:
                self.rules.append(rule)
        else:
            self.rules = newRules
    
    def writeScript(self, filename: str):
        """Write a parsed Droit Database to a Droit Database Script file"""
        _dumper.writeScript(self.rules, filename)
    
    def writeScriptString(self) -> str:
        """Write a parsed Droit Database to a Droit Database Script string"""
        return _dumper.writeScriptString(self.rules)

    def loadPlugins(self, location=_os.path.join(_os.path.dirname(__file__), "plugins"), append=True, preloadScript=True):
        """
        Loads all plugins from the given location and returns them in a
        list containing DroitPlugin items.
        """
        if not(append):
            self.plugins = []

        inList = _os.listdir(path=_os.path.join(location, "input"))
        outList = _os.listdir(path=_os.path.join(location, "output"))
        
        for name in inList:
            if(_os.path.isdir(_os.path.join(location, "input", name))):
                plugin = models.DroitPlugin("input", name, path=location, preloadScript=preloadScript)
                if(plugin.info.req):
                    spec = _importlib.util.spec_from_file_location("pluginReq", _os.path.join(location, "input", name, "req.py"))
                    pl = _importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(pl)
                    members = _inspect.getmembers(pl, predicate=_inspect.isclass)
                    for member in members:
                        if(member[1].__name__ in self.pluginReq.keys()):
                            self.pluginReq[members][member[1].__name__].append(member[1])
                        else:
                            self.pluginReq[member[1].__name__] = [member[1]]

                self.plugins.append(plugin)
        
        for name in outList:
            if(_os.path.isdir(_os.path.join(location, "output", name))):
                self.plugins.append(models.DroitPlugin("output", name, path=location))
    
    def getPluginRequirements(self, plugin: str, func: str):
        """Load requirements provided by other plugins."""
        reqs = []
        for cl in self.pluginReq[plugin.lower()]:
            cl = cl()
            members = _inspect.getmembers(cl, predicate=_inspect.ismethod)
            for member in members:
                if(member[0] == func):
                    function = getattr(cl, func)
                    reqs.append(function)
                    break
        return reqs

    def createVariables(self, vars={}, userinput=None) -> dict:
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
    

    def useRules(self, userinput: models.DroitUserinput) -> _List[models.DroitSearchHit]:
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


    def formatOut(self, hit: models.DroitSearchHit, userinput: models.DroitUserinput) -> str:
        """Evaluates a DroitRuleOutput"""
        output = ""
        variables = self.createVariables(vars=hit.variables, userinput=userinput)

        if not(self.plugins):
            print("Warning: no plugins loaded")

        for i in range(0, len(hit.rule.output)):
            if(hit.rule.output[i].tag.upper() == "EVAL"):
                plugin = ""

                for plug in hit.rule.output[i].children:
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
                    outadd, variables, self = method(params, variables, self)

                    output += outadd
            
            
            else:
                plug = None
                for plugin in self.plugins:
                    if(plugin.mode == "output" and hit.rule.output[i].tag.lower() == plugin.name.lower()):
                        plug = plugin.plugin
                
                if(plug):
                    outadd = ""
                    outadd, variables, self = plug.block(hit.rule.output[i], variables, self)
                    output += outadd
        
        return output
    
    def getInput(*args, **kargs) -> models.DroitUserinput:
        rawInput = self.input(*args, **kargs)
        userinput = models.DroitUserinput(rawInput)
        return userinput

    def simpleIO(self, text: str, history=True) -> str:
        userinput = models.DroitUserinput(text)

        hits = self.useRules(userinput)
        if(hits):
            hit = hits[0]

            output = self.formatOut(hit, userinput)

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
