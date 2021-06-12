# main.py - plugins.output - VAR plugin for python-droit
# Copyright 2020-2021 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def block(rule, variables, db):
    return variables[rule.children[0]], variables, db