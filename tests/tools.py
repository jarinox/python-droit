import droit

try:
    variables = droit.tools.createVariables(inpVars={"inp.test":"mustermann"}, username="Max Mustermann", droitname="Droit", userinput=droit.models.DroitUserinput("Hallo"))
    variables = droit.tools.createVariables()

    plugins = droit.tools.loadPlugins()
    for plugin in plugins:
        if not(plugin.mode.lower() in ["input", "output"]):
            print("test: Warning - plugin '"+plugin.name+"' has invalid mode")

    print("test: 'tools' successful")
except:
    print("test: 'tools' failed")
