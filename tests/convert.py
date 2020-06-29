import droit

# Droit Database Script -> Droit XML
rules1 = droit.loader.parseLegacy("tests/test.dda")
droit.dumper.writeDroitXML(rules1, "tests/dump.xml")
droit.dumper.prettifyXML("tests/dump.xml")

# Droit XML -> Droit Database Script
rules2 = droit.loader.parseDroitXML("tests/dump.xml")
droit.dumper.writeLegacy(rules2, "tests/dump.dda")

# Compare converted databases
rules3 = droit.loader.parseLegacy("tests/dump.dda")

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