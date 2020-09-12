# sample-bot.py - a sample bot using python-droit

import droit

db = droit.Database()
db.loadPlugins()
db.parseScript("german-sample.dda") # or using DroitXML: db.parseDroitXML("german-sample.xml")

running = True

while(running):
    try:
        rawInput = input("Droit> ")
        userinput = droit.models.DroitUserinput(rawInput) # Create DroitUserinput object

        hits = db.useRules(userinput) # Run userinput on database

        if(len(hits) > 0):
            hit = hits[0] # Select the first (best fitting) rule
            variables = db.createVariables(vars=hit.variables, userinput=userinput) #  Create a dict containig variables

            output = db.formatOut(hit.rule.output, variables) #  Generate the output from using an output-rule

            print(output)
        else:
            print("Can't find an answer on this question.")
    except KeyboardInterrupt:
        running = False