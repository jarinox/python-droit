# Documentation - droit.tools
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Functions
- **createVariables**(inpVars={}, username="", droitname="Droit", userinput="")
- **loadPlugins**(location="droit/")


### Function documentation
#### createVariables(inpVars={}, username="", droitname="Droit", userinput="")
Creates useful variables:

- global.time
- global.date
- global.userinput
- global.droitname

Input variables get appended. Returns them all in one dict.

#### loadPlugins(location="droit/")
Loads all plugins from the given location and returns them in a list containing DroitPlugin items. The parameter `location` shows contains the path to the `plugins` folder.