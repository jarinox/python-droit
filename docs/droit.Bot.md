# droit.Bot - Documentation

## Classes
- [Bot](#bot)

## Classes documentation
### Bot
`Bot()` inherits from `pyvnt.EventHost`
#### Properties
- `self.rules` a list of `Rule` objects
- `self.plugins` a dict of `Plugin` objects
- `self.custom` a dict that may be used to pass custom data to e.g. plugins

#### Methods
- `init(self, genOutput: bool = True, loop: bool = True)`  
initializes the bot with standard events (`input_wait`, `input_received`, `output_ready` and `output_sent`). If `loop` is set to `true` an action will be added to `output_sent` that triggers `input_await`.
- `start(self)` starts the bot by triggering `input_await` event.
- `import_rules_from_file(self, path: str)` imports rules from a .dds file.
- `import_rules_from_string(self, string: str, location: str=None)` imports rules from a Droit Database Script string