import droit

rules = droit.loader.parseLegacy("tests/test.dda")
rpack = droit.models.DroitResourcePackage()

success = True

try:
    uips = ["hallo", "wie gehts dir", "wie geht es dir", "wie gehts", "ich heiße max mustermann", "wer bist du", "guten mittag", "du bist cool", "ich mag dich nicht", "ich habe dich gern", "bis bald"]
    dops = [['Hi'], ['Sehr gut!'], ['Sehr gut!'], ['Gut!'], ['Hallo max mustermann'], ['Ich bin Droit'], ['Dir auch einen schönen mittag'], ['Danke du auch!'], [None], ['Ich hab dich auch gern'], ['Tschüss', 'Bis bald', 'Auf wiedersehen']]
    answers = []

    for inp in uips:
        userinput = droit.models.DroitUserinput(inp)
        hits = droit.useRules(rules, userinput, rpack)

        if(len(hits) > 0):
            hit = hits[0]

            variables = droit.tools.createVariables(inpVars=hit.variables, userinput=userinput)
            answer = droit.formatOut(hit.rule.output, variables, rpack)
            answers.append(answer)
        else:
            answers.append(None)

    for i in range(0, len(answers)):
        if not(answers[i] in dops[i]):
            print("test: 'rules' got '" + str(answers[i]) + "', expected '" + str(dops[i]) + "'")
            success = False
except:
    success = False

if success:
    print("test: 'rules' successfull")
else:
    print("test: 'rules' failed")