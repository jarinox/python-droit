# pyvnt.py - event based programming for python
# Copyright 2022 Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)

import asyncio
from typing import Coroutine


class Action:
    def __init__(self, callable, callback=None):
        self.callable = callable
        self.callback = callback

class HostAction:
    def __init__(self, callable):
        self.callable = callable

class ConditionalAction:
    def __init__(self, conditionFn, callable):
        self.conditionFn = conditionFn
        self.callable = callable


class Event:
    def __init__(self):
        self.actions: list[Action] = []


class EventHost:
    def __init__(self):
        self.events = {}

        self._tasks = []
        self._quit: bool = False
        self.createEvent("quit")
    
    async def _start(self, event: str):
        self._tasks.append([self.triggerEvent, [event], {}])
        routines: list[Coroutine] = []

        while(len(routines) > 0 or len(self._tasks) > 0):
            while(len(self._tasks) > 0):
                routines.append(self._tasks[0][0](*self._tasks[0][1], **self._tasks[0][2]))
                self._tasks.pop(0)
                if(self._quit): break

            await asyncio.gather(*routines)
            routines.clear()
            if(self._quit): break

    def start(self, event: str):
        asyncio.run(self._start(event))

    def createEvent(self, name: str):
        self.events[name] = Event()
    
    async def triggerEvent(self, name: str, args=[], kwargs={}) -> bool:
        if name == "quit":
            self._quit = True
            return True
        if name in self.events.keys():
            for action in self.events[name].actions:
                if(isinstance(action, HostAction)):
                    action.callable(self, *args, **kwargs)
                
                elif(isinstance(action, ConditionalAction)):
                    cond = action.conditionFn(*args, **kwargs)
                    if(cond):
                        if(callable(action.callable)):
                            action.callable()
                        elif(isinstance(action.callable, str)):
                            self._tasks.append([
                                self.triggerEvent,
                                [action.callable], {}
                            ])
                        else:
                            raise Exception("Not a callable.")

                elif(isinstance(action, Action)):
                    if(callable(action.callable)):
                        response = action.callable(*args, **kwargs)
                        if(response == (None,)): response = None
                        
                        if(callable(action.callback)):
                            if(response == None):
                                self.callback()
                            else:
                                self.callback(response)
                        else:
                            if(response == None):
                                self._tasks.append([
                                    self.triggerEvent,
                                    [action.callback],
                                    {}
                                ])
                            else:
                                self._tasks.append([
                                    self.triggerEvent,
                                    [action.callback],
                                    {"args": [response]}
                                ])
                    else:
                        self._tasks.append([
                            self.triggerEvent,
                            [action.callable],
                            {}
                        ])
                else:
                    raise Exception("Event.actions may only include Action objects")   
            return True
        return False