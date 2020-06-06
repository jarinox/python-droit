# main.py - plugins.input - SIMT (similar text) plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jaybeejs/python-droit)

import difflib

def block(userinput, inputRules, block, rpack):
    passRule = True
    variables = []
    rankMod = 1

    for j in range(0, len(inputRules)):
        if(block == inputRules[j].tag):
            limit = 0.9
            if("limit" in inputRules[j].attrib.keys()):
                try:
                    limit = float(inputRules[j].attrib["limit"]) / 100
                except:
                    print("python-droit, error: plugins.input.simt, parsing 'limit' attrib failed")

            for child in inputRules[j].children:
                difference = difflib.SequenceMatcher(None, child, userinput.rawInput).ratio()
                if(difference < limit):
                    passRule = False
                    rankMod = 0

    return passRule, variables, rankMod