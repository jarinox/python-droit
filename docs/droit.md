# Documentation for python-droit v1.1
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jarinox/python-droit).


## Submodules
- droit.models
- droit.legacy


## Class
### droit.Database()
**Methods overview**
- parseScript(*filename*, *plugins=True*, *append=False*)
- parseScriptString(*string*, *plugins=True*, *append=False*)
- parseLegacy(*filename*)
- writeScript(*filename*)
- writeScriptString()
- loadPlugins(*location=default*)
- createVariables(*vars={}*, *userinput=None*)
- useRules(*userinput*)
- formatOut(*outputRules*, *variables*):
- simpleIO(*text*, *history=True*)

### Methods
#### parseScript(*filename*, *plugins=True*, *append=False*)
Parses a Droit Database Script file.
- filename: path to file
- plugins: use loaded plugins (if false only supports default plugins), if enabled it is required to run `loadPlugins()` before usage
- append: append to already loaded rules

#### parseScriptString(*string*, *plugins=True*, *append=False*)
Parse Droit Database Script from a string.
Works like `parseScript()`.

#### parseLegacy(*filename*)
Legacy Droit Database Script parsing algorithm.

#### writeScript(*filename*)
Write the parsed rules to a Droit Database Script file.

#### writeScriptString()
Exports the parsed rules to Droit Database Script and returns it as a string.

#### loadPlugins(*location=default*, *append=True*)
Loads plugins from a plugins folder. Default location points to the internal plugins folder that comes with python-droit
- location: path to plugins folder
- append: if true append to already imported plugins (or overwrite if false)

#### createVariables(*vars={}*, *userinput=None*)
Returns a dict containing variables needed by `formatOut()`

#### useRules(*userinput*):
Runs parsed rules onto the userinput and returns all fitting rules sorted by relevance as a list of `models.DroitSearchHit` objects.
- userinput: a `models.DroitUserinput` object

#### formatOut(outputRules, variables)
Evaluates a DroitOutputRule.
- outputRules: a list of `models.DroitOutputRule` objects (e.g. from `models.DroitSearchHit().rules.output`)
- variables: a dict of variables created by `createVariables()`

#### simpleIO(text, history=True)
Simple function for testing databases. Works like a simple bot.
- text: some input string from the user
- history: save result in `self.history` ?