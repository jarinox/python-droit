# Documentation - droit.legacy
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).

This submodule contains functions from python-droit v0.4 to create a backward compatibility of the Droit Database Script. It is NOT recommended to use the functions of this module!

## Functions
- bool **isValidLine**(String *ddaFileLine*)
- List **parseDDA**(String *filename*, \[String *mode="strict"*\])

### Functions documentation

#### bool core.isValidLine(String *ddaFileLine*)
Checks wether a given line from a .dda file is valid DDS script.
Returns `True` or `False`.

#### List parseDDA(String *filename*, \[String *mode="strict"*\])
Don't use this function to parse a DDA file! Use the command droit.loader.parseLegacy() instead!

Parses a .dda file. Mode can be set to `strict` or `fast`. `fast` only checks wether a line contains `->` while `strict` checks for all needed parameters to be given.
Returns a list which contains the .dda file splited up at "\n", "->", ":" and "!".
returnValue\[*line*\]\[*input_or_output*\]\[*block*\]\[*blockname_or_value*\]