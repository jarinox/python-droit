import os as _os
import importlib as _importlib
import json as _json
import random as _random


class Plugin:
    """Load a plugin"""
    def __init__(self, mode: str, name: str, path=_os.path.join(_os.path.dirname(__file__), "plugins")):
        self.mode = mode.lower()
        self.name = name

        self.info: dict = _json.loads(
            open(_os.path.join(path, mode, name, "info.json"), "r").read()
        )

        spec = _importlib.util.spec_from_file_location(
            "main",
            _os.path.join(path, mode, name, "main.py")
        )

        self.plugin = _importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.plugin)

