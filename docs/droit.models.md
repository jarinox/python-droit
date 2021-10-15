# Documentation - droit.models
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jarinox/python-droit).


## Classes
- **DroitCache**()
- **DroitRule**(inputRules, outputRules)
- **DroitRuleInput**(tag, attrib, children)
- **DroitRuleOutput**(tag, children)
- **DroitUserinput**(rawInput)
- **DroitPlugin**(mode, name, path="droit/")
- **DroitPluginInfo**(mode, name, path="droit/")
- **DroitSearchHit**(rule, variables, ranking)
- **DroitHistory**()
- **DroitSession**(username, droitname=False, ident=RANDOM)
- **DroitMultiSession**(path=None, droitname=False)


### Classes documentation
#### DroitCache()
Cache the return value of slow functions.

##### Functions
- **run**(function, *args, **kargs)  
  Returns the value of function() and uses cached vales if available. Hands over *args and **kargs when given.

#### DroitHistory()
List of inputs and outputs of python-droit.

**Attributes**
- inputs: list of [DroitUserinput](#droituserinputrawinput) objects
- outputs: list of output strings
- rules: list of [DroitRule](#droitruleinputrules-outputrules) objects that have been used to get the output from the userinput

##### Functions
- **newEntry**(userinput, rule, output)  
  Creates a new entry in the history
- **loadHistory**(filename)
  Load settings from a json file
- **saveHistory**(filename)
  Save history to a json file


#### DroitRule(inputRules, outputRules)
Stores a list of inputRules and a list of outputRules.

**Attributes**

- input: a list containing `droit.models.DroitRuleInput()` objects
- output: a list containing `droit.models.DroitRuleOutput()` objects

#### DroitRuleInput(tag, attrib, children)
Stores an input rule.

**Attributes**

- tag: tag of the rule e.g. TEXT or INP
- attrib: dict containing the attributes of the rule
- mode: contains String "input"

#### DroitRuleOutput(tag, attrib, children)
Stores an output rule.

**Attributes**

- tag: tag of the rule e.g. VAR or EVAL
- mode: contains String "output"

#### DroitUserinput(rawInput)
Stores the raw userinput as well as a list of the words the userinput consists of. The list is created on init.

**Attributes**

- rawInput: the raw userinput as a string
- simpleInput: lowercase version of raw userinput with unnecessary characters removed
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

#### DroitSearchHit(rule, variables, ranking)
List item returned by `useRules()`

**Attributes**

- rule: a [DroitRule()](#droitruleinputrules-outputrules)
- variables: dict containing variables
- ranking: int index showing relevancen

#### DroitSession(username, droitname=False, ident=RANDOM)
Stores a user-session.

**Attributes**
- id: identifier of user
- username
- droitname: optional, only use if not set within DroitMultiSession
- userData: dict that can be used to store some data about the user between sessions

**Functions**
- fromDict(var)
- toDict()

#### DroitMultiSession(path=None, droitname=False)
Stores sessions.

**Attributes**
- sessions: list containing `DroitSession` objects
- active: list index of active session (or `-1` when inactive)
- droitname
- path: path to file to store sessions in

**Functions**
- loadSessions()
- saveSessions()
- getActive()
- activateById(id)
- activateByUsername(username)
- setActive(session)