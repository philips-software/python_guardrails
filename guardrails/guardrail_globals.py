"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
from __future__ import print_function
import sys
from configparser import ConfigParser
import os
import itertools

if (2, 7, 0) <= sys.version_info < (3, 5, 7):
    import glob2  # for python 2.7
elif sys.version_info >= (3, 5, 7):
    import glob


class GuardrailGlobals:
    """  This is a class for holding and pre processing guardrails globals. """

    def __init__(self):
        """  default constructor for the class"""
        self.src_folder = None
        self.lint_buffer = 20
        self.test_folder = None
        self.pytest = None
        self.report_folder = None
        self.jscpd_root = None
        self.cyclo_exclude = None
        self.python = None
        self.pylintrc = None
        self.covrc = None
        self.dup_token = 100
        self.min_deadcode_confidence = 60
        self.percent_cov = None
        self.allow_dup = None
        self.cc_limit = None
        self.allow_mutants = None
        self.all_folders = None
        self.linting = True
        self.cpd = True
        self.cov = True
        self.mutation = True
        self.deadcode = True
        self.cycloc = True
        self.programming_language = None
        self.jscpd_ignore = None
        self.dead_code_ignore = None
        self.dead_code_whitelist = None

    @staticmethod
    def __get_abs_path(path_ini, input_path):
        """ Function to generate absolute path from relative """
        return os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(path_ini)),
                         input_path))

    def set_all(self, path_ini, buffer):
        """
        Function to set the global variables from thr guardrail.ini

        Parameters:
          path_ini (string): The path to guardrail.ini file.
          buffer (int): Bugger size/number of path for the pylint argument
          split.
        """
        config = ConfigParser()
        if not os.path.exists(path_ini):
            print("please provide valid guardrail.ini file \n\n")
            sys.exit(1)
        config.read(path_ini)
        # folders
        self.src_folder = self.__get_abs_path(path_ini,
                                              config.get('folder',
                                                         'source_folder'))
        self.test_folder = self.__get_abs_path(path_ini,
                                               config.get('folder',
                                                          'test_folder'))
        self.pytest = self.__get_abs_path(path_ini,
                                          config.get('folder',
                                                     'pytest_root'))
        self.report_folder = self.__get_abs_path(path_ini,
                                                 config.get('folder',
                                                            'report_folder'))
        self.jscpd_root = self.__get_abs_path(path_ini,
                                              config.get('folder',
                                                         'jscpd_root'))
        # python
        self.python = (config.get('python', 'python'))
        if not ((config.get('python', 'pylint_rc_file')).strip()):
            self.pylintrc = (config.get('python', 'pylint_rc_file'))
        else:
            self.pylintrc = self.__get_abs_path(path_ini,
                                                config.get('python',
                                                           'pylint_rc_file'))
            # coverage
        if not ((config.get('coverage', 'coverage_rc_file')).strip()):
            self.pylintrc = (config.get('coverage', 'coverage_rc_file'))
        else:
            self.covrc = self.__get_abs_path(path_ini,
                                             config.get('coverage',
                                                        'coverage_rc_file'))
        # gates
        self.dup_token = (config.getint('gates', 'jscpd_duplicate_token'))
        self.percent_cov = (config.getint('gates', 'coverage_percentage'))
        self.allow_dup = (config.getint('gates', 'jscpd_allowed_duplication'))
        self.cc_limit = (
            config.getint('gates', 'cyclomatic_complexity_allowed'))
        self.allow_mutants = (
            config.getint('gates', 'allowed_mutants_percentage'))
        self.min_deadcode_confidence = (
            config.getint('gates', 'min_deadcode_confidence'))
        # options
        self.linting = (config.getboolean('options', 'linting'))
        self.cpd = (config.getboolean('options', 'cpd'))
        self.cov = (config.getboolean('options', 'coverage'))
        self.mutation = (config.getboolean('options', 'mutation'))
        self.deadcode = (config.getboolean('options', 'deadcode'))
        self.cycloc = (config.getboolean('options', 'cyclomatic_complexity'))
        # others
        self.programming_language = (
            config.get('others', 'programming_language'))
        # ignores
        self.cyclo_exclude = (
            config.get('ignore', 'cyclomatic_complexity_exclude'))
        self.dead_code_ignore = (config.get('ignore', 'dead_code_ignore'))
        self.jscpd_ignore = (config.get('ignore', 'jscpd_ignore'))

        if not ((config.get("ignore", "dead_code_whitelist")).strip()):
            self.dead_code_whitelist = (config.get("ignore",
                                                   "dead_code_whitelist"))
        else:
            self.dead_code_whitelist = self.__get_abs_path(
                path_ini, (config.get("ignore", "dead_code_whitelist")))
        # post processing
        self.all_folders = self.src_folder + " " + self.test_folder
        self.lint_buffer = buffer

    def mutable_lint_cmd(self):
        """ Function to parse and form optional linting command
         (ignore files and rc file) """

        cmd = ""
        if self.pylintrc:
            cmd = cmd + " " + "--rcfile %s" % self.pylintrc
        return cmd

    def generate_pylint_cmd(self):
        """ Function to set optional linting command
         (ignore files and rc file) """
        cmd_list = []
        sub_list = [self.generate_files_lint()[i:i + self.lint_buffer]
                    for i in
                    range(0, len(self.generate_files_lint()), self.lint_buffer)]
        for i, _ in enumerate(sub_list):
            cmd_list.append(
                "%s -m pylint  %s --output-format=parseable %s" % (
                    self.python, self.list_to_str(sub_list[i]),
                    self.mutable_lint_cmd()))
        return cmd_list

    def get_exclude_cc(self):
        """ Function which is used to construct the exclude string for
         cyclomatic complexity of lizard"""
        cmd = ""
        if self.cyclo_exclude:
            exclude = self.cyclo_exclude.rstrip('\n')
            cmd = " -x ".join(
                [str(item).rstrip('\n') for item in str(exclude).split(',')])
            cmd = "-x " + cmd + " "
        return cmd

    def jscpd_format(self):
        """ Function to set optional jscpd command to set the
         format to be ckecked """
        cmd = ""
        if self.programming_language:
            cmd = '--format "%s"' % self.programming_language
        return cmd

    def jscpd_ignore_file(self):
        """ Function to set optional jscpd command ignore file """
        cmd = ""
        if self.jscpd_ignore:
            cmd = "--ignore %s" % self.jscpd_ignore
        return cmd

    def cov_rc_file(self):
        """ Function to set optional coverage command to set
         the coverage config file"""
        cmd = ""
        if self.covrc:
            cmd = "--cov-config=%s" % self.covrc
        return cmd

    def dead_code_exclude(self):
        """ Function to set optional vulture command to set the ignore files """
        cmd = ""
        if self.dead_code_ignore:
            cmd = "--exclude %s" % self.dead_code_ignore
        return cmd

    @staticmethod
    def list_to_str(str_list):
        """ Function to convert ignored pylint files list to string """
        list_in_string = ' '.join(str(e) for e in str_list)
        return list_in_string

    def generate_files_lint(self):
        """ Function to get ignored pylint files """
        res = None
        if self.all_folders.split():
            lint_input_list = []
            for item in self.all_folders.split():
                if (2, 7, 0) <= sys.version_info < (3, 5, 7):
                    src_lint_file = glob2.glob(
                        r'%s%s**%s*.py' % (item, os.sep, os.sep))  # for 2.7
                elif sys.version_info >= (3, 5, 7):
                    src_lint_file = glob.iglob(
                        r'%s%s**%s*.py' % (item, os.sep, os.sep),
                        recursive=True)
                src_input_list = [item for item in src_lint_file]
                lint_input_list.append(src_input_list)
            input_list = list(
                set(list(itertools.chain.from_iterable(lint_input_list))))
            res = input_list
        return res
