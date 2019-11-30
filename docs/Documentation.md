# core.py - documentation

**Attention:** To fully understand this documentation you need to know about Droit and the Droit Database Script (DDS) in general. If you don't know about DDS please read its' documentation first.

## Methods
- bool **isValidLine**(String *ddaFileLine*)
- List **parseDDA**(String *filename*, \[String *mode="strict"*\])
- List **prepareInput**(String *userinput*)
- List **useRules**(List *rules*, String *userinput*, ResourcePackage *rpack=None*)
- List **createVariables**(List *inpVars=[]*, String *username="unknown"*, String *droitname="Droit"*, String *userinput=""* )
- String **runOutputPlugin**(String *plugin*, List *variables*, ResourcePackage *rpack=None*)
- String **formatOut**(List *outRules*, List *variables*, ResourcePackage *rpack=None*)
- String **simpleIO**(String *userinput*, String *databasePath*)

## Method Documentation
#### bool core.isValidLine(String *ddaFileLine*)
Checks wether a given line from a .dda file is valid DDS script.
Returns `True` or `False`.

#### List parseDDA(String *filename*, \[String *mode="strict"*\])
Parses a .dda file. Mode can be set to `strict` or `fast`. `fast` only checks wether a line contains `->` while `strict` checks for all needed parameters to be given.
Returns a list which contains the .dda file splited up at "\n", "->", ":" and "!".
returnValue\[*line*\]\[*input_or_output*\]\[*block*\]\[*blockname_or_value*\]

#### List prepareInput(String *userinput*)
Removes unneccesarry characters from userinput and splits it up at spaces.

#### List useRules(List *rules*, String *userinput*, ResourcePackage *rpack=None*)
Uses rules gathered with `parseDDA()` on an userinput which was prepared with `prepareInput()`.
Returns a list of all possible output-rules sorted by relevance.

#### List createVariables(List *inpVars=[]*, String *username="unknown"*, String *droitname="Droit"*, String *userinput=""* )
Creates a list of variables. To the optionally given input-variables there are several variables added:

- global.time
- global.date
- global.username
- global.droitname
- global.userinput

#### String runOutputPlugin(String *plugin*, List *variables*, ResourcePackage *rpack=None*)
Runs a plugin and returns the plugins return value.
The string *plugin* is the text given after the exclamation mark of the `EVAL` block.

#### String formatOut(List *outRules*, List *variables*, ResourcePackage *rpack=None*)
Runs the output-rules and returns an answer. Therefore it needs variables prepared by `createVariables()`.

#### String simpleIO(String *userinput*, String *databasePath*)
Can be used to build a very simple chat bot. Uses the userinput on a given .dda file and returns an answer. It runs throug all the methods explained aboth.


## Classes
- ResourcePackage(*gmrModule=None*, *gmrDatabase=None*)

## Class Documentation
#### ResourcePackage(*gmrModule=None*, *gmrDatabase=None*)
Package to provide the initialized grammar module to the plugins.
