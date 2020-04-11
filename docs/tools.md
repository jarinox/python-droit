# Documentation - droit.tools
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Class
- **SettingsObject**()

### Class documentation
#### SettingsObject()
**Functions**

- loadSettings() - loads settings from file to the settings attribute
- saveSettings() - saves the settings from the attribute to the file
- initSettings() - creates a config file to store the settings inside

**Attribute**

- settings - a dict containing some settings

## Function
- **createVariables(inpVars={}, username="", droitname="Droit", userinput="")**

### Function documentation
#### createVariables(inpVars={}, username="", droitname="Droit", userinput="")
Creates useful variables:

- global.time
- global.date
- global.userinput
- global.droitname

Input variables get appended. Returns them all in one dict.