# main.py - plugins.output - TEXT plugin for python-droit
# Copyright 2020-2021 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def block(rule, variables, db):
    output = ""
    for item in rule.children:
        output += item + ","
    output = output[:-1]
    return output, variables, db