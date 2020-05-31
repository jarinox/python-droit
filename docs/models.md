# Documentation - droit.models
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Classes
- **DroitSettings**(location="")
- **DroitResourcePackage**()
- **DroitRule**(inputRules, outputRules)
- **DroitRuleInOut**(tag, attrib, children, mode)
- **DroitUserinput**(rawInput)
- **DroitPlugin**(mode, name, path="droit/")
- **DroitPluginInfo**(mode, name, path="droit/")

### Classes documentation
#### DroitSettings(location="")
Read and write settings from and to config.json  
  
**Functions**

- loadSettings() - loads settings from file to the settings attribute
- saveSettings() - saves the settings from the attribute to the file
- initSettings() - creates a config file to store the settings inside

**Attribute**

- settings - a dict containing some settings

#### DroitResourcePackage()
Provides useful tools and information to any part of python-droit.

**Attributes**

- settings: [droit.models.DroitSettings()](#droitsettingslocation)
- io: [droit.io.DroitIO()](https://github.com/jaybeejs/python-droit/blob/master/docs/io.md)
- tools: [droit.tools](https://github.com/jaybeejs/python-droit/blob/master/docs/tools.md)
- plugins: a list containing [droit.models.DroitPlugin()](#droitpluginmode-name) items

#### DroitRule(inputRules, outputRules)
Stores a list of inputRules and a list of outputRules.

**Attributes**

- input: a list containing [droit.models.DroitRuleInOut()](#droitruleinouttag-attrib-children-mode) items
- output: a list containing [droit.models.DroitRuleInOut()](#droitruleinouttag-attrib-children-mode) items

#### DroitRuleInOut(tag, attrib, children, mode)
Stores an input-rule or an output-rule.

**Attributes**

- mode: specifies wether this object contains an input-rule or an output-rule (String "input" or String "output")
- tag: tag of the rule e.g. TEXT, INP or EVAL
- attrib: dict containing the attributes of the rule
- children: a list containing the children of the rule

#### DroitUserinput(rawInput)
Stores the raw userinput as well as a list of the words the userinput consists of. The list is created on init.

**Attributes**

- rawInput: the raw userinput as a string
- words: processed list containig the words of the raw userinput

#### DroitPlugin(mode, name, path="droit/")
Loads a plugin.

**Attributes**

- mode: "input" or "output"
- name: name of the plugin e.g. "text" or "inp"
- plugin: contains the plugin

#### DroitPluginInfo(mode, name, path="droit/")
Loads info from input plugin.

**Attributes**

- mode: "input" or "output"
- name: name of the plugin e.g. "text" or "inp"
- attrib: contains a list of possible attributes
- description: a short description of the plugin
