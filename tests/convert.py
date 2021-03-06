import droit
import copy

db = droit.Database()

# Droit Database Script -> Droit XML
db.parseScript("tests/test.dda")
rules1 = copy.deepcopy(db.rules)
droit.legacy.writeDroitXML(db.rules, "tests/dump.xml")

# Droit XML -> Droit Database Script
db.rules = droit.legacy.parseDroitXML("tests/dump.xml")
rules2 = copy.deepcopy(db.rules)
db.writeScript("tests/dump.dda")

# Compare converted databases
db.parseScriptString(open("tests/dump.dda", "r").read(), plugins=False)
rules3 = copy.deepcopy(db.rules)

success = True

# Test info parsing
if not(db.info.license == ["CC0"] and db.info.author == ["Jakob Stolze"]):
    success = False
    print("test: 'convert' info parsing failed")


if not(len(rules1) == len(rules2) and len(rules1) == len(rules3)):
    success = False
    print("test: 'convert' invalid rules length")
else:
    for i in range(0, len(rules1)):
        for j in range(0, len(rules1[i].input)):
            if not(rules1[i].input[j].tag == rules2[i].input[j].tag and rules1[i].input[j].tag == rules3[i].input[j].tag):
                success = False
                print("test: 'convert' invalid tags")
            if not(rules1[i].input[j].children == rules2[i].input[j].children and rules1[i].input[j].children == rules3[i].input[j].children):
                success = False
                print("test: 'convert' invalid children")
            if not(rules1[i].input[j].attrib == rules2[i].input[j].attrib and rules1[i].input[j].attrib == rules3[i].input[j].attrib):
                success = False
                print("test: 'convert' invalid attributes")
            if not(rules1[i].input[j].mode == rules2[i].input[j].mode and rules1[i].input[j].mode == rules3[i].input[j].mode):
                success = False
                print("test: 'convert' invalid modes")


db.parseScript("tests/dump.dda", append=True)
if not(len(db.rules) == len(rules3) * 2):
    print("test: 'convert' append doesn't work")
    success = False


if success:
    print("test: 'convert' successful")
else:
    print("test: 'convert' failed")