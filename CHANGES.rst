###############
Version History
###############

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`_
and this project adheres to `Semantic Versioning <http://semver.org/>`_.

Version: Unreleased
===============================================================================

ADDED
-----

  * setUpFeature/tearDownFeature, setUpScenario/tearDownScenario, setUpStep/tearDownStep (#105)
  * hiding irrelevant morelia's code from tracebacks (#111)
  * new recommended "verify" function with API simpler than in run (#118)

CHANGED
-------

  * dropped support for setUp/tearDown executed before/after each scenario (#105)

Version: 0.8.3 (2019-04-16)
===============================================================================

FIXED
-----

  * attribute error when comment on first line after scenario (#116)

Version: 0.8.2 (2019-04-12)
===============================================================================

FIXED
-----

  * incorrectly matching steps in languages other than english (#113)
  * incorrect matching methods with parse format (#106).

Version: 0.8.1 (2019-04-11) [YANKED]
===============================================================================

FIXED
-----

  * incorrect matching methods with parse format (#106).


Version: 0.8.0 (2019-02-09)
===============================================================================

REMOVED
-------

  * dropped support for python 2.7 and 3.4


Version: 0.7.1 (2019-01-15)
===============================================================================

ADDED
-----

  * support for running single scenarios (#16)
  * support for passing string to morelia.run instead of external feature file

REMOVED
-------

  * dropped support for python 3.3


Version: 0.6.5 (2016-10-12)
===============================================================================

CHANGED
-------

  * added new line before printing Feature


Version: 0.6.3 (2016-07-10)
===============================================================================

CHANGED
-------

  * removed ReportVisitor
  * removed branching on multiple When's

FIXED
-----

  * error while reporting missing steps


Version: 0.6.2 (2016-06-10)
===============================================================================

FIXED
-----

  * incorrect handling labels inside steps

Version: 0.6.1 (2016-03-29)
===============================================================================

FIXED
-----

  * regression in reporting unicode exceptions

Version: 0.6.0 (2016-03-28)
===============================================================================

ADDED
-----

  * reporting on all failing scenarios

Version: 0.5.2 (2016-02-21)
===============================================================================

CHANGED
-------

  * by default all missing steps are now shown

FIXED
-----

  * rendering issues in README.rst and docs

Version: 0.5.1 (2016-02-20)
===============================================================================

FIXED
-----

  * bug with setUp/tearDown methods called twice
  * bug with double run of background steps when show_all_missing=True


Version: 0.5.0 (2015-05-30)
===============================================================================

ADDED
-----

  * labels in feature files
  * tags decorator
  * step's text payload


Version: 0.4.2 (2015-05-10)
===============================================================================

FIXED
-----

  * bug with matching utf-8 docstrings with unicode predicate


Version: 0.4.1 (2015-05-07)
===============================================================================

FIXED
-----

  * bug with comments support in scenarios with tables


Version: 0.4.0 (2015-04-26)
===============================================================================

ADDED
-----

  * support for Background keyword
  * support for different output formatters
  * Examples keyword as no-op

CHANGED
-------

  * folding missing steps suggestions for more condense output

Version: 0.3.0 (2015-04-14)
===============================================================================

ADDED
-----

  * support for matching methods by str.format-like ({name}) docstrings
  * example project

CHANGED
-------

  * showing all missing steps instead of only first

Version: 0.2.1 (2015-04-06)
===============================================================================

ADDED
-----

  * support for Python 3
  * native language support
