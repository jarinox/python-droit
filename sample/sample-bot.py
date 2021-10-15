# sample-bot.py - a sample bot using python-droit

import droit

db = droit.Database()
db.loadPlugins()
db.parseScript("german-sample.dda") # or db.parseScript("english-sample.dda")

running = True

while(running):
    try:
        userinput = db.getInput("Droit> ") # Runs db.input (which defaults to the python input() function) and returns a models.DroitUserinput object
        # The line above is equal to:
        # rawInput = input("Droit> ")
        # userinput = droit.models.DroitUserinput(rawInput)

        hits = db.useRules(userinput) # Run userinput on database

        if(len(hits) > 0):
            hit = hits[0] # Select the first (best fitting) rule
            output = db.formatOut(hit, userinput) #  Generate the output from using an output-rule

            print(output)
        else:
            print("Can't find an answer on this question.")
    except KeyboardInterrupt:
        running = False