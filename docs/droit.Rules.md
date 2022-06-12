# droit.Rules - Documentation

## Classes
- [Rule](#rule)
- [Subrule](#subrule)
- [Meta](#meta)

## Classes documentation
### Rule
`Rule()`  
`Rule.from_script(script: str)`

#### Properties
- `self.input` a list of `Subrule` objects
- `self.output` a list of `Subrule` objects
- `self.meta` a `Meta` object

### Subrule
`Subrule()`  
`Subrule.from_script(script: str)`

#### Properties
- `self.name` the name (`str`) of the rule
- `self.args` a list of arguments (`list[str]`)
- `self.values` a list of values (`list[str]`)
- `self.operator` an operator character (one out of `|&!^%`)

Example:
```
NAME*arg1*arg2*argsAreOptional|value1,value2,valuesAreOptional
```
`NAME` is the name of the rule. `["arg1","arg2","argsAreOptional"]` is the list of arguments. `|` is the operator. `["value1","value2","valuesAreOptional"]` is the list of values.

### Meta
`Meta(self, location=None, attribs={})`  
#### Properties
- `self.location` is the path of the `.dds` file the script was imported from
- `self.attribs` is a dict of metadata from the file
- `self.author` is `self.attribs["author"]`
- `self.ddsVersion` is `self.attribs["dds"]`