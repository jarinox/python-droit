import droit

db = droit.Database()

# Droit Database Script -> Droit XML
db.parseLegacy("tests/test.dda")
rules1 = db.rules
db.writeDroitXML("tests/dump.xml")

# Droit XML -> Droit Database Script
db.parseDroitXML("tests/dump.xml")
rules2 = db.rules
db.writeLegacy("tests/dump.dda")

# Compare converted databases
db.parseLegacy("tests/dump.dda")
rules3 = db.rules

success = True

if not(len(rules1) == len(rules2) and len(rules1) == len(rules3)):
    success = False
else:
    for i in range(0, len(rules1)):
        for j in range(0, len(rules1[i].input)):
            if not(rules1[i].input[j].tag == rules2[i].input[j].tag and rules1[i].input[j].tag == rules3[i].input[j].tag):
                success = False
            if not(rules1[i].input[j].children == rules2[i].input[j].children and rules1[i].input[j].children == rules3[i].input[j].children):
                success = False
            if not(rules1[i].input[j].attrib == rules2[i].input[j].attrib and rules1[i].input[j].attrib == rules3[i].input[j].attrib):
                success = False
            if not(rules1[i].input[j].mode == rules2[i].input[j].mode and rules1[i].input[j].mode == rules3[i].input[j].mode):
                success = False

if success:
    print("test: 'convert' successful")
else:
    print("test: 'convert' failed")