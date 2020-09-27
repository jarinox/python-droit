import droit

# Init database
db = droit.Database(multiSession=True)
db.loadPlugins()
db.parseScript("tests/test.dda")

# Load sessions
db.sessions.path = "tests/sessions.json"
db.sessions.loadSessions()
db.sessions.activateByUsername("Max Mustermann")

success = True

def sio(inp):
    userinput = droit.models.DroitUserinput(inp)
    hits = db.useRules(userinput)

    if(len(hits) > 0):
        hit = hits[0]
        answer = db.formatOut(hit, userinput)
        db.history.newEntry(userinput, hit, answer)
        return answer
    else:
        db.history.newEntry(userinput, None, None)
        return None


# Test cache
answer1 = db.cache.run(sio, param1="Wer bin ich")
answer2 = db.cache.run(sio, param1="Wer bin ich")

if not(answer1 == answer2):
    print("test: 'models' cache not working")
    success = False

if not(answer1 == "Du bist Max Mustermann"):
    print("test: 'models' got '" + answer1 + "', expected 'Du bist Max Mustermann'")
    success = False

# Test history and cache
if(len(db.history.outputs) != 1):
    success = False

# Test history
sio("Wie geht es dir")
if(db.history.outputs[1] != "Sehr gut!"):
    print("test: 'models' history not working")
    success = False


if success:
    print("test: 'models' successful")
else:
    print("test: 'models' failed")