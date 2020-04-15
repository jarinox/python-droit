# Documentation - droit.models
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Classes
- **DroitResourcePackage**()
- **DroitRule**(inputRules, outputRules)
- **DroitRuleInOut**(tag, attrib, children, mode)
- **DroitUserinput**(rawInput)
- **DroitPlugin**(mode, name)

### Classes documentation
#### DroitResourcePackage()
Provides useful tools and information to any part of python-droit.

**Attributes**

- settings: droit.tools.SettingsObject()
- io: droit.tools.io()
- tools: droit.tools
- plugins: a list containing droit.models.DroitPlugin() items

#### DroitRule(inputRules, outputRules)
Stores a list of inputRules and a list of outputRules.

**Attributes**

- input: a list containing droit.models.DroitRuleInOut() items
- output: a list containing droit.models.DroitRuleInOut() items

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

#### DroitPlugin(mode, name)
Loads a plugin.

**Attributes**

- mode: "input" or "output"
- name: name of the plugin e.g. "text" or "inp"
- plugin: contains the plugin
