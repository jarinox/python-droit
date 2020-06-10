# Documentation for python-droit
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Submodules
Each submodule has it's own documentation.

- [droit.loader](https://github.com/jaybeejs/python-droit/blob/master/docs/loader.md)
- [droit.dumper](https://github.com/jaybeejs/python-droit/blob/master/docs/dumper.md)
- [droit.models](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md)
- [droit.tools](https://github.com/jaybeejs/python-droit/blob/master/docs/tools.md)
- [droit.io](https://github.com/jaybeejs/python-droit/blob/master/docs/io.md)
- [droit.legacy](https://github.com/jaybeejs/python-droit/blob/master/docs/legacy.md)

## Functions

- **useRules**(rules, userinput, rpack, rback=False)
- **formatOut**(outputRules, variables, rpack, rback=False)
- **simpleIO**(rawInput, databasePath)

### Functions documentation
#### useRules(rules, userinput, rpack, rback=False)
Runs each entry of a Droit Database onto the userinput and returns all possible output-rules sorted by relevance.

**Parameters:**
- rules: a list containing [droit.models.DroitRule()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitruleinputrules-outputrules) items
- userinput: a [droit.models.DroitUserinput()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droituserinputrawinput)
- rpack: a [droit.models.DroitResourcePackage()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitresourcepackagesettingsnone-plugins)

**Returns:** If `rback` is set to `False`: a list containing [droit.models.DroitSearchHit()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitsearchhit-rule-variables-ranking) items  
  
If `rback` is set to `True` it returns a tuple containing ([droit.models.DroitSearchHit()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitsearchhit-rule-variables-ranking), [droit.models.DroitResourcePackage()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitsearchhit-rule-variables-ranking))


#### formatOut(outputRules, variables, rpack, rback=False)
Runs output-rules and returns an answer string.

**Parameters:**
- outputRules: a list containing [droit.models.DroitRuleInOut()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitruleinouttag-attrib-children-mode) items
- variables: a dict containing read-in variables from useRules. It is recommended to prepare those with [droit.tools.createVariables()](https://github.com/jaybeejs/python-droit/blob/master/docs/tools.md#createvariablesinpvars-username-droitnamedroit-userinput)
- rpack: a [droit.models.DroitResourcePackage()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitresourcepackagesettingsnone-plugins)

**Returns:** If `rback` is set to `False`: an answer string  
If `rback` is set to `True`: a tuple (output, rpack)


#### simpleIO(rawInput, databasePath)
Runs the full process from loading a database to returning an answer. This function is intended to be used for testing databases. It is NOT recommended to use this function for building bots.

**Parameters:**
- rawInput: raw userinput as a string
- databasePath: path to a xml droit database

**Returns:** an answer string