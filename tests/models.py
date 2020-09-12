import droit

db = droit.Database()
db.loadPlugins()
db.parseScript("tests/test.dda")

db.settings.location = "tests/config.json"
db.settings.loadSettings()

success = True

def sio(inp):
    userinput = droit.models.DroitUserinput(inp)
    hits = db.useRules(userinput)

    if(len(hits) > 0):
        hit = hits[0]

        variables = db.createVariables(vars=hit.variables, userinput=userinput)
        answer = db.formatOut(hit.rule.output, variables)
        db.history.newEntry(userinput, hit, answer)
        return answer
    else:
        db.history.newEntry(userinput, None, None)
        return None


# Test cache
answer1 = db.cache.run(sio, param1="Wer bin ich")
answer2 = db.cache.run(sio, param1="Wer bin ich")

if not(answer1 == answer2 and answer2 == "Du bist Max Mustermann"):
    success = False

# Test history and cache
if(len(db.history.outputs) != 1):
    success = False

# Test history
sio("Wie geht es dir")
if(db.history.outputs[1] != "Sehr gut!"):
    success = False


if success:
    print("test: 'models' successful")
else:
    print("test: 'models' failed")