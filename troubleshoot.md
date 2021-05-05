The tool parses all the folders & subfolders given in the test and source directory to fetch out all the .py files to pass to pylint. 
This is to ovecome the limitation of pylint not running on folders which doesnot contain __init__.py file.

The tool by default takes 20 files at a time for linting. This is to limit the input argument length to the pylint. At any given if there are 
too many inout arguments or the argument input buffer overflows, you are free to change the number of input files passed to the pylint by changing 
commandline option

'''python -m guardrails --p path\to\guardrail.ini --b #number (defaulted to 20)''' 