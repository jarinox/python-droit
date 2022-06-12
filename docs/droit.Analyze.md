# droit.Analyze - Documentation

## Methods
- [`extract_metadata(line: str) -> tuple`](#extractmetadata)
- [`isValidLine(line: str) -> bool`](#isvalidline)

## Methods documentation
### extract_metadata
`extract_metadata(line: str) -> tuple`  
Extracts metadata from a line of Droit Database Script.  
For `@dds 2.0` returns e.g. `("dds", "2.0")`. If line is no metadata returns `(None, None)`

### isValidLine
`is_valid_line(line: str) -> bool`  
Checks whether a given line is valid Droit Database Script. Comments are not considered as valid.