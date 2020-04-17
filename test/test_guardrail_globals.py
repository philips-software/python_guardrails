""" This file does the  test of the "guardrails_globals """

import unittest
from unittest.mock import MagicMock
from guardrails.guardrail_globals import GuardrailGlobals


class TestGuardrailGlobal(unittest.TestCase):
    """ Class to test the logging and command line input feature """

    def test_mutable_lint_cmd_string(self):
        """Function to test mutable_lint_cmd_string method"""
        global_obj = GuardrailGlobals()
        global_obj.lint_ignore = "abc"
        global_obj.pylintrc = "xyz"
        returnval = global_obj.mutable_lint_cmd()
        self.assertEqual(returnval, "--ignore abc --rcfile xyz")

    def test_mutable_lint_cmd_empty(self):
        """Function to test mutable_lint_cmd_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.lint_ignore = None
        global_obj.pylintrc = None
        returnval = global_obj.mutable_lint_cmd()
        self.assertEqual(returnval, "")

    def test_generate_pylint_cmd_empty(self):
        """Function to test generate_pylint_cmd_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.linting = None
        global_obj.mutable_lint_cmd = MagicMock(return_value="xyz")
        returnval = global_obj.generate_pylint_cmd()
        self.assertEqual(returnval, "")

    def test_generate_pylint_cmd_string(self):
        """Function to test generate_pylint_cmd_string method"""
        global_obj = GuardrailGlobals()
        global_obj.linting = "abc"
        global_obj.python = "python"
        global_obj.mutable_lint_cmd = MagicMock(return_value="xyz")
        returnval = global_obj.generate_pylint_cmd()
        self.assertEqual(returnval, "python -m pylint  xyz")

    def test_get_exclude_cc_empty(self):
        """Function to test get_exclude_cc_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.cyclo_exclude = None
        returnval = global_obj.get_exclude_cc()
        self.assertEqual(returnval, "")

    def test_get_exclude_cc_string(self):
        """Function to test get_exclude_cc_string method"""
        global_obj = GuardrailGlobals()
        global_obj.cyclo_exclude = "test, sample"
        returnval = global_obj.get_exclude_cc()
        self.assertEqual(returnval, "-x test/* -x  sample/*")

    def test_get_exclude_jscpd_empty(self):
        """Function to test get_exclude_jscpd_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.programming_language = None
        returnval = global_obj.jscpd_format()
        self.assertEqual(returnval, "")

    def test_get_exclude_jscpd_string(self):
        """Function to test get_exclude_jscpd_string method"""
        global_obj = GuardrailGlobals()
        global_obj.programming_language = "python"
        returnval = global_obj.jscpd_format()
        self.assertEqual(returnval, '--format "python"')

    def test_jscpd_ignore_file_string(self):
        """Function to test jscpd_ignore_file_string method"""
        global_obj = GuardrailGlobals()
        global_obj.jscpd_ignore = "python"
        returnval = global_obj.jscpd_ignore_file()
        self.assertEqual(returnval, '--ignore python')

    def test_jscpd_ignore_file_empty(self):
        """Function to test jscpd_ignore_file_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.jscpd_ignore = None
        returnval = global_obj.jscpd_ignore_file()
        self.assertEqual(returnval, '')

    def test_cov_rc_file_empty(self):
        """Function to test cov_rc_file_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.covrc = None
        returnval = global_obj.cov_rc_file()
        self.assertEqual(returnval, '')

    def test_cov_rc_file_string(self):
        """Function to test cov_rc_file_string method"""
        global_obj = GuardrailGlobals()
        global_obj.covrc = "None"
        returnval = global_obj.cov_rc_file()
        self.assertEqual(returnval, '--cov-config=None')

    def test_dead_code_exclude_string(self):
        """Function to test dead_code_exclude_string method"""
        global_obj = GuardrailGlobals()
        global_obj.dead_code_ignore = "None"
        returnval = global_obj.dead_code_exclude()
        self.assertEqual(returnval, '--exclude None')

    def test_dead_code_exclude_empty(self):
        """Function to test dead_code_exclude_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.dead_code_ignore = None
        returnval = global_obj.dead_code_exclude()
        self.assertEqual(returnval, '')

    def test_init(self):
        """Function to test init method"""
        global_obj = GuardrailGlobals()
        # self.assertEqual(global_obj.config, None)
        self.assertEqual(global_obj.src_folder, None)
        self.assertEqual(global_obj.test_folder, None)
        self.assertEqual(global_obj.pytest, None)
        self.assertEqual(global_obj.report_folder, None)
        self.assertEqual(global_obj.cyclo_exclude, None)
        self.assertEqual(global_obj.python, None)
        self.assertEqual(global_obj.pylintrc, None)
        self.assertEqual(global_obj.covrc, None)
        self.assertEqual(global_obj.dup_token, 50)
        self.assertEqual(global_obj.percent_cov, None)
        self.assertEqual(global_obj.allow_dup, None)
        self.assertEqual(global_obj.cc_limit, None)
        self.assertEqual(global_obj.allow_mutants, None)
        self.assertEqual(global_obj.all_folders, None)
        self.assertEqual(global_obj.linting, True)
        self.assertEqual(global_obj.cpd, True)
        self.assertEqual(global_obj.cov, True)
        self.assertEqual(global_obj.mutation, True)
        self.assertEqual(global_obj.deadcode, True)
        self.assertEqual(global_obj.cycloc, True)
        self.assertEqual(global_obj.lint_ignore, None)
        self.assertEqual(global_obj.programming_language, None)
        self.assertEqual(global_obj.jscpd_ignore, None)
        self.assertEqual(global_obj.dead_code_ignore, None)

    def test_set_all(self):
        """Function to test set_all method"""
        import os
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        ini_path = os.path.join(ini_path, "test_resource", "guardrail.ini")
        global_obj = GuardrailGlobals()
        global_obj.set_all(ini_path)
        # self.assertEqual(global_obj.config, None)
        self.assertEqual(global_obj.src_folder,
                         r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\functiondefextractor")
        self.assertEqual(global_obj.test_folder, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test")
        self.assertEqual(global_obj.pytest, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor")
        self.assertEqual(global_obj.report_folder, r"C:\Projects\PythonRepo\REPORT")
        self.assertEqual(global_obj.cyclo_exclude, r"cyclo\excludes")
        self.assertEqual(global_obj.python, r"mypython")
        self.assertEqual(global_obj.pylintrc, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.pylintrc")
        self.assertEqual(global_obj.covrc, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.coveragerc")
        self.assertEqual(global_obj.dup_token, 20)
        self.assertEqual(global_obj.percent_cov, 85)
        self.assertEqual(global_obj.allow_dup, 5)
        self.assertEqual(global_obj.cc_limit, 10)
        self.assertEqual(global_obj.allow_mutants, 30)
        self.assertEqual(global_obj.all_folders,
                         r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\functiondefextractor "
                         r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test")
        self.assertEqual(global_obj.linting, True)
        self.assertEqual(global_obj.cpd, True)
        self.assertEqual(global_obj.cov, True)
        self.assertEqual(global_obj.mutation, True)
        self.assertEqual(global_obj.deadcode, True)
        self.assertEqual(global_obj.cycloc, True)
        self.assertEqual(global_obj.lint_ignore, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test")
        self.assertEqual(global_obj.programming_language, "python, java")
        self.assertEqual(global_obj.jscpd_ignore, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test")
        self.assertEqual(global_obj.dead_code_ignore, r"C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test")


if __name__ == '__main__':
    unittest.main()
