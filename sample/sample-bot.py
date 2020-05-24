# sample-bot.py - a sample bot using python-droit
#
# MOVE THIS FILE TO THE ROOT FOLDER OF PYTHON-DROIT!
# Otherwise it won't be able to import the module "droit"


import droit

rules = droit.loader.parseDroitXML("sample/german-sample.xml") # Load database

settings = droit.models.DroitSettings() # Get settings from config.json
plugins = droit.tools.loadPlugins() # Load plugins

rpack = droit.models.DroitResourcePackage(settings=settings, plugins=plugins) # Create object containig plugins and settings


running = True

while(running):
    try:
        rawInput = rpack.io.input("Droit> ") # Get input from the currently active input/output module
        userinput = droit.models.DroitUserinput(rawInput) # Create DroitUserinput object

        outRules = droit.useRules(rules, userinput, rpack=rpack) # Run userinput on database

        if(len(outRules) > 0):
            outRule = outRules[0] # Select the first (best fitting) rule
            variables = droit.tools.createVariables(inpVars=outRule[1], userinput=userinput) #  Create a dict containig variables

            output = droit.formatOut(outRule[0], variables, rpack=rpack) #  Generate the output from using an output-rule

            rpack.io.output(output) # Output the output-text using the currently active input/output module
        else:
            rpack.io.output("Can't find an answer on this question.")
    except KeyboardInterrupt:
        running = False