# Changelog
All notable changes to this project will be documented in this file.

## master
### Changed
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