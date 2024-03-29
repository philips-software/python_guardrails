![Python application](https://github.com/philips-software/python_guardrails/workflows/Python%20application/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/philips-software/python_guardrails/branch/master/graph/badge.svg)](https://codecov.io/gh/philips-software/python_guardrails)

Guardrails for python projects
=============================

What is the project intended to solve?
-------------------------------------
Project will help to consolidate clean coding practices at the developers desk by a single call which consolidates
 (linting, copy paste detection, Dead code, Test coverage, Cyclomatic complexity, Mutation testing)

Technology stack
---------------
1. Python with few python packages
2. jscpd `https://www.npmjs.com/package/jscpd`

Dependencies
------------
```
Python 3.8
NodeJS 10
JSCPD 3.2.1
```

[packages]

```
pip

mutmut

pytest

Lizard

vulture

codecov

pytest-cov

pylint

glob2
```


Install, Usage & Configuration
--------------------
1. Install the tool using `pip install guardrails`
2. Install jscpd `https://www.npmjs.com/package/jscpd`
3. update the `guardrail.ini` file, content of which is listed below
``` 
[folder]
# Fields under folder config are mandatory, if not provided, 
# will be considering the path of this ini file

# Comma seperated source folders if more than one directory
source_folder = .\EagleVision\eaglevision
# Comma seperated test folders if more than one directory
test_folder = .\EagleVision\test
pytest_root = .\EagleVision\test
report_folder = ..\opensource\python_guardrails\guardrails_report
jscpd_root = .\EagleVision

[python]
python = python
# path to the .pylintrc file if specific linting or leave empty after =
pylint_rc_file = .\EagleVision\.pylintrc

[coverage]
# path to the .coveragerc file if specific cverage config or leave empty after =
coverage_rc_file =

[gates]
# gate values are absolute integers
# duplicate to ken count
jscpd_duplicate_token = 20
# Jscpd allowed % duplication
jscpd_allowed_duplication = 7
# coverage gating %
coverage_percentage = 85
# Allowed mutats %
allowed_mutants_percentage = 20
# cyclomatic complexity allowed value
cyclomatic_complexity_allowed = 10
# minimum deadcode confidence
min_deadcode_confidence = 50

[ignore]
# pylint ignore to be added in the pylintrc file
# Add files or directories matching the regex patterns to the blacklist. The
# regex matches against base names, not paths.
# Ignore all .py files under the 3rdparty subdirectory.

# ignore-patterns=**/3rdparty/**/*.py

# Comma seperated folders if more than one directory or leave empty after = for example cyclomatic_complexity_exclude = "*guardrails.py", "*guardrail_globals.py"
# more details @https://pypi.org/project/lizard/1.17.7/
cyclomatic_complexity_exclude =
# Comma seperated source folders if more than one directory or leave empty after = for example jscpd_ignore = "**/*.min.js,**/*.map"
# More details @ https://www.npmjs.com/package/jscpd#ignored-blocks
jscpd_ignore = 
# Comma seperated source folders if more than one directory or leave empty after = for example If you want to ignore a whole file or directory, use the --exclude parameter (e.g., --exclude *settings.py,docs/
# more details @ https://pypi.org/project/vulture/#description
dead_code_ignore =

# whitelist deadcode (relative path to whitelist.py) [.\path\whitelist.py] or leave it empty after = 
dead_code_whitelist = 

[others]
# Comma seperated language if more than one, for CPD reporting
programming_language = python

[options]
# option can be either true or false
linting=false
cpd=false
coverage=false
mutation=false
deadcode=false
cyclomatic_complexity=false
```
4. To call from commandline
```
python -m guardrails --p path\to\guardrail.ini #ini file created for respective project
```
Sample execution report
----------------------
```
#####Guardrails for python programs#####
Passed linting gate
====================================
Execution Time: 111.103ms
Passed JSCPD gating
====================================
================================================= test session starts =================================================
platform win32 -- Python 3.7.3, pytest-4.6.9, py-1.8.0, pluggy-0.12.0
rootdir: C:\public_repo\python_guardrails
plugins: allure-pytest-2.8.5, cov-2.7.1, html-2.0.1, metadata-1.8.0, pylint-0.14.1
collected 1 item

test\test_sample.py .                                                                                            [100%]

----------- coverage: platform win32, python 3.7.3-final-0 -----------
Coverage HTML written to dir Sample_proj_cov


============================================== 1 passed in 0.19 seconds ===============================================
Passed testing using pytest
====================================
Name                 Stmts   Miss  Cover
----------------------------------------
source\__init__.py       0      0   100%
source\sample.py         3      0   100%
----------------------------------------
TOTAL                    3      0   100%
Passed test coverage gating
====================================

- Mutation testing starting -

These are the steps:
1. A full test suite run will be made to make sure we
   can run the tests successfully and we know how long
   it takes (to detect infinite loops for example)
2. Mutants will be generated and checked

Results are stored in .mutmut-cache.
Print found mutants with `mutmut results`.

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests needs to be expanded.

mutmut cache is out of date, clearing it...
1. Running tests without mutations
⠇ Running... Done

2. Checking mutants
⠹ 2/2  🎉 2  ⏰ 0  🤔 0  🙁 0
Passed mutation testing gate
====================================
Passed Dead code gating
====================================
Passed Cyclomatic complexity gating
====================================
```
Report & Log
-----------
- Report will be collected at the `report_folder` folder mentioned in the guardrail.ini file
- Log file will be generated inside the guardrails package installation with name `guardrails.log`

Contact / Getting help
----------------------
[MAINTAINERS.md](MAINTAINERS.md)

License
--------
[License.md](License.md)