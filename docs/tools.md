# Documentation - droit.tools
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Functions
- **createVariables**(inpVars={}, username="", droitname="Droit", userinput="")
- **loadPlugins**(location="droit/")
- **loadPluginInfos**(location="droit/")


### Function documentation
#### createVariables(inpVars={}, username="", droitname="Droit", userinput="")
Creates useful variables:

- global.time
- global.date
- global.userinput
- global.droitname

Input variables get appended. Returns them all in one dict.

#### loadPlugins(location="droit/")
Loads all plugins from the given location and returns them in a list containing [droit.models.DroitPlugin()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitpluginmode-name) items. The parameter `location` shows contains the path to the `plugins` folder.

#### loadPluginInfos(location="droit/")
Loads a list containing [droit.models.DroitPluginInfo()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitplugininfomode-name) items.