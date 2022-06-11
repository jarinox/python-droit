# Rules.py - Rule classes for Droit Database Script
# Copyright 2022 Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


OPERATORS = "|&!^%"

class Meta:
    """Metadata of a Droit Database Script file."""
    def __init__(self, location=None, attribs={}):
        self.location = location
        self.attribs = attribs
        
        self.author = None
        if("author" in self.attribs.keys()):
            self.author = self.attribs["author"]
        self.ddsVersion = "2.0"
        if("dds" in self.attribs.keys()):
            self.ddsVersion = self.attribs["dds"]


class Subrule:
    """Stores a subrule"""
    def __init__(self):
        self.name: str = ""
        self.args: list[str] = []
        self.values: list[str] = []
        self.operator: str = "|"

    @classmethod
    def from_script(cls, script: str):
        rule = cls()

        mode = 0
        cache = script[0]
        for i in range(1, len(script)):
            if mode == 0 or mode == 1:
                if script[i] == "*" and script[i-1] != "\\":
                    if mode == 0:
                        rule.name = cache
                    else:
                        rule.args.append(cache)
                        mode = 1
                    cache = ""
                elif script[i] in OPERATORS and script[i-1] != "\\":
                    rule.operator = script[i]
                    rule.name = cache
                    cache = ""
                    mode = 2
                    continue
                else:
                    cache += script[i]
            if mode == 2:
                if script[i] == "," and script[i-1] != "\\":
                    rule.values.append(cache)
                    cache = ""
                else:
                    cache += script[i]
        if len(cache) > 0 and mode == 2:
            rule.values.append(cache)

        return rule
    
    def to_script(self) -> str:
        script = self.name
        if len(self.args) > 0:
            script += "*" + "*".join(self.args)
        script += self.operator
        if len(self.values) > 0:
            script += ",".join(self.values)
        return script
    


class Rule:
    """Stores a rule"""
    def __init__(self):
        self.input: list[Subrule] = []
        self.output: list[Subrule] = []
        self.meta = None

    # Import rule from Droit Database Script
    @classmethod
    def from_script(cls, script: str, meta: Meta=None):
        rule = cls()
        rule.meta = meta

        inMode = True
        cache = script[0]
        for i in range(1, len(script)):
            if inMode:
                if script[i-1] == "-" and script[i] == ">":
                    rule.input.append(
                        Subrule.from_script(cache[:-1])
                    )
                    cache = ""
                    inMode = False
                elif script[i] == ":" and script[i-1] != "\\":
                    rule.input.append(
                        Subrule.from_script(cache)
                    )
                    cache = ""
                else:
                    cache += script[i]
            else:
                if script[i] == ":" and script[i-1] != "\\":
                    rule.output.append(
                        Subrule.from_script(cache)
                    )
                    cache = ""
                else:
                    cache += script[i]
        if len(cache) > 0:
            rule.output.append(
                Subrule.from_script(cache)
            )

        return rule

    # Export rule to Droit Database Script
    def to_script(self) -> str:
        script = ":".join(
            [rule.to_script() for rule in self.input]
        )
        
        script += "->" + ":".join(
            [rule.to_script() for rule in self.output]
        )

        return script