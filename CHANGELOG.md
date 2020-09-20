# Changelog
All notable changes to this project will be documented in this file.

| Latest release | Version of this branch |  
|----------------|------------------------|
| 1.0.3          | 1.1.0:4 alpha          |


## 1.1.0:4
### Changed
- `preloadScript` was added to input plugins
- all parsing functions have the new optional parameter `append=False` which allows to append the parsed rules to the current rules

### Removed
- `parseDroitXML` and `writeDroitXML` were removed. However they will still be available in the legacy submodule (`legacy.parseDroitXML`)

## 1.1.0:1-3
### Added
- new DDS parsing algorithm used by the new functions `parseScript` and `parseScriptString`
- `writeScriptString` makes it possible dump a Droit Database to a DDS string

### Changed
- `writeLegacy` method name was changed to `writeScript`
- `DroitRuleInOut` was split up to `DroitRuleInput` and `DroitRuleOutput`
- `legacy.checkValidLine()` improved
- tests changed to use `parseScript`

## 1.1.0 alpha
Droit v1.1 and v1.0 are not compatible. The Database formats haven't changed but the library uses different commands and objects so you will have to rewrite you bot but you will still be able to use your old databases.
### 1. Database object
A new object called `Database` will be now the core of python-droit. It combines the functionallity of `__init__.py`, `tools.py`, `loader.py` and `dumper.py` from Droit v1.0. You can use it to parse and dump a Database, you can load plugins into it and run `useRules()` and `formatOut()` from it. It replaces `rpack` as it also stores the `settings`, `cache` and `history` objects.

### 2. Plugins
Restructuring droit of caurse has an effect on the plugins. There are minimal adjustments that have to be done to make v1.0 plugins work with v1.1. The biggest change is that there are now two types of output plugins. On the one hand there are still those that are called using `EVAL`. The folder they are stored in is from now on called `eval.pluginName`. The new type of output plugins is similar to input plugins. Those plugins use a `block()` function. The `TEXT` and `VAR` blocks are no longer part of the core source code but plugins.

### 3. DroitIO
DroitIO will be removed as it is the task of the person who writes the bot to implement a solution for input and output. Probably there will be a ready-to-use bot based on python-droit soon that can be configured easily similar to what DroitIO offered.

## 1.0.3 release
### Changed
- fix [#25](https://github.com/jarinox/python-droit/issues/25) formatOut bug when using EVAL
- test "rules" improved
- test "tools" improved
- imports fixed

## 1.0.2 release
### Added
- [#24](https://github.com/jarinox/python-droit/issues/24) type annotations added
- test "tools" added
- test "io" added
- tests introduced: "convert", "models" and "rules" tests added

### Changed
- tools.createVariables bug fixed
- "Droit" as standard droitname in `config.json`
- imports fixed
- [#23](https://github.com/jarinox/python-droit/issues/22) make package pypi compatible

## 1.0.1 release
### Changed
- fix [#22](https://github.com/jarinox/python-droit/issues/22) block rule name

## 1.0.0 release
### Added
- class `DroitHistory` added to `droit.models`
- class `DroitCache` added to `droit.models`
- telegram io module added

### Changed
- [#21](https://github.com/jaybeejs/python-droit/issues/21) class `DroitUserinput` has new attribute `simpleInput`
- fix [#20](https://github.com/jaybeejs/python-droit/issues/20) rules ranking
- `formatOut()` optionally returns `rpack` - the `rpack` parameter is no longer optional
- [#19](https://github.com/jaybeejs/python-droit/issues/19) output plugins return rpack
- `useRules()` optionally returns `rpack` - the `rpack` parameter is no longer optional
- class `DroitResourcePackage` has new attribute `history` which contains a `DroitHistory` object
- class `DroitResourcePackage` has new attribute `cache` which contains a `DroitCache` object
- [#17](https://github.com/jaybeejs/python-droit/issues/17) input plugins return rpack

## 1.0.0 pre1
### Added
- class `DroitSearchHit` added to `droit.models`

### Changed
- `useRules()` returns now a list containing `DroitSearchHit` items
- fix [#15](https://github.com/jaybeejs/python-droit/issues/15) `INP` plugin bug
- fix [#16](https://github.com/jaybeejs/python-droit/issues/15) Droit Database Script parser