[![Build Status](https://travis-ci.com/philips-software/python_guardrails.svg?branch=master)](https://travis-ci.com/philips-software/python_guardrails)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/philips-software/python_guardrails/branch/master/graph/badge.svg)](https://codecov.io/gh/philips-software/python_guardrails)

Guardrails for python projects
=============================

What is the project intented to solve?
-------------------------------------
Project will help to consolidate clean coding practices at the developers desk by a single call which consolidates
 (linting, copy paste
 detection, Dead code, Test coverage, Cyclomatic complexity, Mutation testing)

Technology stack
---------------
1. Python with few python packages
2. jscpd `https://www.npmjs.com/package/jscpd`

Dependencies
------------
```
Python 3.7.3
NodeJS 10
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
```


Install, Usage & Configuration
--------------------
1. Install the tool using `pip install guardrails`
2. Install jscpd `https://www.npmjs.com/package/jscpd`
3. update the `guardrail.ini` file, content of which is listed below
``` 
[folder]
# Comma seperated source folders if more than one directory
source_folder = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\function_def_extractor 
# Comma seperated test folders if more than one directory
test_folder = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test
pytest_root = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor
report_folder = C:\Projects\PythonRepo\REPORT

[python]
python = python
# path to the .pylintrc file if specific linting or leave empty after =
pylint_rc_file = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.pylintrc

[coverage]
# path to the .coveragerc file if specific cverage config or leave empty after =
coverage_rc_file = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.coveragerc

[gates]
# gate values are absolute integers
# duplicate to ken count
jscpd_duplicate_token = 20
# Jscpd allowed % duplication
jscpd_allowed_duplication = 5
# coverage gating %
coverage_percentage = 95
# Allowed mutats %
allowed_mutants_percentage = 20
# cyclomatic complexity allowed value
cyclomatic_complexity_allowed = 10

[ignore]
# Comma seperated folders if more than one directory or leave empty after =
cyclomatic_complexity_exclude =  C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test_resource, C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test
# Comma seperated source folders if more than one directory or leave empty after =
pylint_ignore = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test
# Comma seperated source folders if more than one directory or leave empty after =
jscpd_ignore = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test
# Comma seperated source folders if more than one directory or leave empty after =
dead_code_ignore = C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test

[others]
# Comma seperated language if more than one
programming_language = python, java

[options]
# option can be either true or false
linting=true
cpd=true
coverage=true
mutation=true
deadcode=true
cyclomatic_complexity=true
```
4. To call from commandline
```
python -m guardrails.guardrails --p path\to\guardrail.ini #ini file created for respective project
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