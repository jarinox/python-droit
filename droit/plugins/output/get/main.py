# main.py - plugins.output - GET plugin for python-droit
# Copyright 2021 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def block(rule, variables, db):
    varname = "default"
    if len(rule.children) > 1:
        q = ",".join(rule.children[1:])
        varname = rule.children[0]
    else:
        q = ",".join(rule.children)
    inp = db.input(q)
    variables["get." + varname] = inp
    return "", variables, db