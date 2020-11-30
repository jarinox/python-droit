# Documentation - droit.analyzer
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jarinox/python-droit).

The analyzer helps you to find errors within your Droit Datbase Script and to fix them.

## Functions
- String **upgradeScript**(String *script*)
- bool **isValidLine**(String *line*, bool *infos=False*)
- Dict **parseScriptInfoString**(String *script*)


### Functions documentation
#### String upgradeScript(String *script*)
This function upgrades a legacy Droit Database Script to the current version. This function will be extended with every change in the Droit Database Script.

#### bool isValidLine(String *line*, bool *infos=False*)
Checks wether a given line is valid Droit Database Script.


#### Dict parseScriptInfoString(String *script*)
This function was previously located within the `loader` module. It reads the metadata from a Droit Database Script into a dict.
