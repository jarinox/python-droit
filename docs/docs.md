# Documentation for python-droit
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Submodules
Each submodule has it's own documentation.

- droit.loader
- droit.dumper
- droit.legacy
- droit.models
- droit.tools
- droit.io

## Functions

- **useRules**(rules, userinput, rpack=None)
- **formatOut**(outputRules, variables, rpack=None)
- **simpleIO**(rawInput, databasePath)

### Functions documentation
#### useRules(rules, userinput, rpack=None)
Runs each entry of a Droit Database onto the userinput and returns all possible output-rules sorted by relevance.

**Parameters:**
- rules: a list containing droit.models.DroitRule() items
- userinput: a droit.models.DroitUserinput()
- rpack: a droit.models.DroitResourcePackage()

**Returns:** a list containing droit.models.DroitRuleInOut() items


#### formatOut(outputRules, variables, rpack=None)
Runs output-rules and returns an answer string.

**Parameters:**
- outputRules: a list containing droit.models.DroitRuleInOut() items
- variables: a dict containing read-in variables from useRules. It is recommended to prepare those with droit.tools.prepareVariables()
- rpack: a droit.models.DroitResourcePackage()

**Returns:** an answer string


#### simpleIO(rawInput, databasePath)
Runs the full process from loading a database to returning an answer. This function is intended to be used for testing databases. It is NOT recommended to use this function for building bots.

**Parameters:**
- rawInput: raw userinput as a string
- databasePath: path to a xml droit database

**Returns:** an answer string