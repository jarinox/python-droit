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

        hits, rpack = droit.useRules(rules, userinput, rpack, rback=True) # Run userinput on database

        if(len(hits) > 0):
            hit = hits[0] # Select the first (best fitting) rule
            variables = droit.tools.createVariables(inpVars=hit.variables, userinput=userinput) #  Create a dict containig variables

            output, rpack = droit.formatOut(hit.rule.output, variables, rpack, rback=True) #  Generate the output from using an output-rule

            rpack.io.output(output) # Output the output-text using the currently active input/output module
        else:
            rpack.io.output("Can't find an answer on this question.")
    except KeyboardInterrupt:
        running = False