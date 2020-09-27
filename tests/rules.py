import droit

db = droit.Database()
db.loadPlugins()
db.parseScript("tests/test.dda")

success = True

try:
    uips = ["hallo", "wie gehts dir", "wie geht es dir", "wie gehts", "ich heiße max mustermann", "wer bist du", "guten mittag", "du bist cool", "ich mag dich nicht", "ich habe dich gern", "bis bald", "tut mir leid"]
    dops = [['Hi'], ['Sehr gut!'], ['Sehr gut!'], ['Gut!'], ['Hallo max mustermann'], ['Ich bin Droit'], ['Dir auch einen schönen mittag'], ['Danke, du auch!'], [None], ['Ich hab dich auch gern'], ['Tschüss', 'Bis bald', 'Auf wiedersehen'], ["Kein Problem!", "Ist ok!"]]
    answers = []

    for inp in uips:
        userinput = droit.models.DroitUserinput(inp)
        hits = db.useRules(userinput)

        if(len(hits) > 0):
            hit = hits[0]

            answer = db.formatOut(hit, userinput)
            answers.append(answer)
        else:
            answers.append(None)

    for i in range(0, len(answers)):
        if not(answers[i] in dops[i]):
            print("test: 'rules' got '" + str(answers[i]) + "', expected '" + str(dops[i]) + "'")
            success = False

    answers = []

    # testing it with simpleIO
    for inp in uips:
        answers.append(db.simpleIO(inp))

    for i in range(0, len(answers)):
        if not(answers[i] in dops[i]):
            print("test: 'rules' got '" + str(answers[i]) + "', expected '" + str(dops[i]) + "' (simpleIO)")
            success = False


except:
    success = False
    raise

if success:
    print("test: 'rules' successful")
else:
    print("test: 'rules' failed")