# python-droit
Droit is a simple library for creating bots

**THIS BRANCH CONTAINS AN EXPERIMENTAL VERSION OF DROIT**  
Droit 1.1.0 alpha  

## What's new about Droit v1.1?
### 1. Database object
A new object called `Database` will be now the core of python-droit. It combines the functionallity of `__init__.py`, `tools.py`, `loader.py` and `dumper.py` from Droit v1.0. You can use it to parse and dump a Database, you can load plugins into it and run `useRules()` and `formatOut()` from it. It replaces `rpack` as it also stores the `settings`, `cache` and `history` objects.

### 2. Plugins
Restructuring droit of caurse has an effect on the plugins. There are minimal adjustments that have to be done to make v1.0 plugins work with v1.1. The biggest change is that there are now two types of output plugins. On the one hand there are still those that are called using `EVAL`. The folder they are stored in is from now on called `eval.pluginName`. The new type of output plugins is similar to input plugins. Those plugins use a `block()` function. The `TEXT` and `VAR` blocks are no longer part of the core source code but plugins.

### 3. DroitIO
DroitIO will be removed as it is the task of the person who writes the bot to implement a solution for input and output. Probably there will be a ready-to-use bot based on python-droit soon that can be configured easily similar to what DroitIO offered.
  
## Stable version of python-droit
This branch is under heavy development. Please use a stable version of python-droit!
- Latest release: [Version 1.0.3](https://github.com/jarinox/python-droit/releases/tag/v1.0.3)

This library is published under the terms of the GNU LESSER GENERAL PUBLIC LICENSE. Please see LICENCE for more information.  
Copyright 2019-2020 Jakob Stolze
