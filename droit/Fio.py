from droit.Rules import Meta, Rule, Subrule
from droit.Analyze import extract_metadata, isValidLine


def from_string(dds: str, location=None) -> list[Rule]:
    lines = dds.split("\n")
    attribs = {}
    for line in lines:
        key, value = extract_metadata(line)
        if(key):
            attribs[key] = value
    
    meta = Meta(attribs=attribs, location=location)
    rules = []

    for line in lines:
        if isValidLine(line):
            rules.append(
                Rule.from_script(line, meta=meta)
            )

    return rules

def from_file(path: str):
    with open(path, "r") as f:
        return from_string(f.read(), location=path)