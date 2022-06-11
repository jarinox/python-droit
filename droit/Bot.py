# Bot.py - a python-droit bot
# Copyright 2022 Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

from droit.Rules import Rule
from droit.pyvnt import Action, EventHost
from droit.Plugins import Plugin

from droit.Fio import from_file as _from_file, from_string as _from_string



class Bot(EventHost):
    """A python-droit bot"""
    def __init__(self):
        super().__init__()

        self.rules: list[Rule] = []
        self.plugins: dict[Plugin] = {}

        self.custom = {}
    

    def init(self, genOutput: bool = True, loop: bool = True):
        """Initializes bot with standard events and actions."""
        self.createEvent("input_await")
        self.createEvent("input_received")
        self.createEvent("output_ready")
        self.createEvent("output_sent")

        if genOutput:
            self.events["input_received"].actions.append(
                Action(self.answer, "output_ready")
            )
        
        if loop:
            self.events["output_sent"].actions.append(
                Action("input_await")
            )
    
    def start(self):
        """Starts the bot by triggering 'input_await' event."""
        super().start("input_await")

    def import_rules_from_file(self, path: str):
        """Import rules from a .dds file."""
        self.rules += _from_file(path)
    
    def import_rules_from_string(self, string: str, location: str=None):
        """Import rules from a Droit Database Script string."""
        self.rules += _from_string(string, location=location)

    def useRules(self, input) -> list[Rule]:
        pass

    def formatOut(self, input, rule: Rule) -> str:
        """Evaluates an output-rule."""
        pass

    def answer(self, input) -> str:
        """Generate an answer from an input using the imported rules and plugins"""
        hits = self.useRules(input)
        if len(hits) > 0:
            return self.formatOut(input, hits[0])
        return False
