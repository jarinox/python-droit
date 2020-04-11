# Documentation - droit.loader
Your can find the source-code of python-droit and this documentation on [Github](https://github.com/jaybeejs/python-droit).


## Functions
- **parseDroitXML**(filename)
- **parseLegacy**(filename)

### Functions documentation
#### parseDroitXML(filename)
Parses a XML Droit Database v1.0
Returns a list containing droit.models.DroitRule() items.

#### parseLegacy(filename)
Parses a legacy Droit Database v0.4 and tries to apply the new v1.0 structure on it. You can use this together with droit.dumper.writeDroitXML() to convert a legacy Droit Database v0.4 to a XML Droit Database v1.0.