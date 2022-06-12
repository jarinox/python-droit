# pyvnt - Documentation
pyvnt is a library for event-based programming in python.


## Classes
- [Action](#action)
- [ConditionalAction](#conditionalaction)
- [HostAction](#hostaction)
- [Event](#event)
- [EventHost](#eventhost)

## Classes documentation
### Action
`Action(callable: function|str, callback: function|str=None)`  
#### Properties
- `self.callable` a callable or a string. If set to a callable the function will be evaluated when the event is triggered the action is assigned to. If set to a string the event with this name will be triggered.
- `self.callback` a callable or string. The function or event will receive the result of `self.callable` after it was evaluated. This property may only be set if `self.callable` is a function.

### ConditionalAction
`ConditionalAction(conditionFn: function, callable: function|str)`  
#### Properties
- `self.conditionFn` is a callable that returns a boolean value.
- `self.callable` will be evaluated if `self.conditionFn` returns true. Can be a callable of a string (event name).

### HostAction
`HostAction(callable: function)`  
#### Properties
- `self.callable` is a callable. When evaluated the function gets the `EventHost` object passed as first parameter.

### Event
`Event()`  
#### Properties
- `self.actions: list[Action]` is a list of actions that will be evaluated simultaniously when the event is triggered.

### EventHost
`EventHost()`  
#### Properties
- `self.events: dict[str, event]` a dict of events registered on the host.

#### Methods
- `start(self, event: str) -> None` triggers an initial event.
- `createEvent(self, event: str)` creates an empty event
- `async def triggerEvent(self, name: str, args=[], kwargs={}) -> bool` triggers an event and runs all of it actions simultaniously. This function may only be called by other events. Otherwise use `start(self, event: str)`.