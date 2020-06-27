import droit

rules = droit.loader.parseLegacy("tests/test.dda")

settings = droit.models.DroitSettings(location="tests/")
plugins = droit.tools.loadPlugins()
rpack = droit.models.DroitResourcePackage(settings=settings, plugins=plugins)

success = True

def sio(inp):
    global rpack
    userinput = droit.models.DroitUserinput(inp)
    hits, rpack = droit.useRules(rules, userinput, rpack, rback=True)

    if(len(hits) > 0):
        hit = hits[0]

        variables = droit.tools.createVariables(inpVars=hit.variables, userinput=userinput, username=rpack.settings.settings["username"])
        answer, rpack = droit.formatOut(hit.rule.output, variables, rpack, rback=True)
        rpack.history.newEntry(userinput, hit, answer)
        return answer
    else:
        rpack.history.newEntry(userinput, None, None)
        return None


# Test cache
answer1 = rpack.cache.run(sio, param1="Wer bin ich")
answer2 = rpack.cache.run(sio, param1="Wer bin ich")

if not(answer1 == answer2 and answer2 == "Du bist Max Mustermann"):
    success = False

# Test history and cache
if(len(rpack.history.outputs) != 1):
    success = False

# Test history
sio("Wie geht es dir")
if(rpack.history.outputs[1] != "Sehr gut!"):
    success = False


if success:
    print("test: 'models' successfull")
else:
    print("test: 'models' failed")