# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### (will be 2.2.2)

* added CentOS 8 support (mostly Requires and BuildRequires changes)
* __init__.py - setting to stronger SSL by default

## [2.2.1] - 2019-08-19

### Changed

* ran all python through flake8 python linter, cleaned it up to match

### Changed

## [2.2.0] - 2019-08-16

* puppetdb-report-usage - added disk data
* converted all scripts and libraries to Python 3.

## [2.1.4] - 2019-03-19

### Added

* CHANGELOG.md - standardizing on a single changelog file

### Changed

* Makefile.local - now includes Pypi (pip) bindings
* setup.py, omdclient.spec - re-worked for setuptools instead of distutils.core
* README.md - lots of updates on the path towards real distribution
* `usr/sbin/*` moved to `usr/bin/*` (it just plays nicer with python)

