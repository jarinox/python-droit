# Documentation - droit.loader
You can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Functions
- **parseDroitXML**(filename)
- **parseLegacy**(filename)

### Functions documentation
#### parseDroitXML(filename)
Parses a XML Droit Database v1.0
Returns a list containing [droit.models.DroitRule()](https://github.com/jaybeejs/python-droit/blob/master/docs/models.md#droitruleinputrules-outputrules) items.

#### parseLegacy(filename)
Parses a legacy Droit Database v0.4 and tries to apply the new v1.0 structure on it. You can use this together with [droit.dumper.writeDroitXML()](https://github.com/jaybeejs/python-droit/blob/master/docs/dumper.md#writedroitxmldda-filename) to convert a legacy Droit Database v0.4 to a XML Droit Database v1.0.