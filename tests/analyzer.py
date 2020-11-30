import droit

success = True

success = droit.analyzer.isValidLine("A!value:B!value->C!value")
if(success):
    success = not(droit.analyzer.isValidLine("A->B"))
if(success):
    success = not(droit.analyzer.isValidLine("*A!->A!"))
if(success):
    success = droit.analyzer.isValidLine("A*a!->XYZ!a")
if not(success):
    print("test: analyzer: isValidLine doesn't work")
else:
    success = (droit.analyzer.upgradeScript("@dds 1.1\nTEXT!ich->TEXT!Du&arz;") == "@dds 1.1\nTEXT!ich->TEXT!Du\\!")
    if(success):
        success = (droit.analyzer.upgradeScript("@dds 1.2\nTEXT!ich->TEXT!Du&arz;") == "@dds 1.2\nTEXT!ich->TEXT!Du&arz;")
    if not(success):
        print("test: analyzer: upgradeScript doesn't work")    


if success:
    print("test: 'analyzer' successful")
else:
    print("test: 'analyzer' failed")