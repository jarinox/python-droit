# Documentation - droit.dumper
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Functions
- **writeDroitXML**(dda, filename)
- **prettifyXML**(filename)#
- **writeLegacy**(dda, filename)

### Functions documentation
#### writeDroitXML(dda, filename)
Write a parsed Droit Database to Droit XML v1.0  
**Parameter:** dda: a list containing [droit.models.DroitRule()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitruleinputrules-outputrules) items

#### prettifyXML(filename)
Converts the XML from the given file to be more readable.

#### writeLegacy(dda, filename)
Write a parsed Droit Database to Droit Database Script  
**Parameter:** dda: a list containing [droit.models.DroitRule()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitruleinputrules-outputrules) items
