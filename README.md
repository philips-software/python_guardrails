
Guardrails for python projects
=============================

What is the project intented to solve?
-------------------------------------
Project will help to consolidate clean coding guardrails in a single call which consolidates (linting, Copy paste
 detection, Dead code, Test coverage, Cyclomatic complexity, Mutation testing)

Technology stack
---------------
1. Python with few python packages
2. jscpd `https://www.npmjs.com/package/jscpd`

Dependencies
------------
`Python 3.7.3`

[packages]
**************
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


Usage & Configuration
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
# option can be either trur or false
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

Contact / Getting help
----------------------
`brijesh.krishnank@philips.com`

License
--------
```
The MIT License (MIT) Copyright © [2019] Koninklijke Philips N.V, https://www.philips.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED AS IS,  WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
 WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


```
