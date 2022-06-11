# Analyze.py - analyze Droit Database Script snippets
# Copyright 2020-2022 Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

def extract_metadata(line: str):
    if(len(line) > 3):
        if(line[0] == "@"):
            spl = line.split(" ")
            if(len(spl) > 1):
                return spl[0][1:], " ".join(spl[1:])
    return None, None

def isValidLine(line: str) -> bool:
    valid = len(line) > 5
    if valid:
        valid = valid and "->" in line
        valid = valid and line[0] != "@"
    if valid:
        parts = line.split("->")
        valid = valid and len(parts) == 2
    return valid
