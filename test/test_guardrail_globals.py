"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import unittest
from unittest.mock import MagicMock
from guardrails.guardrail_globals import GuardrailGlobals


class TestGuardrailGlobal(unittest.TestCase):
    """ Class to test the logging and command line input feature """

    def test_mutable_lint_cmd_empty(self):
        """Function to test mutable_lint_cmd_empty method"""
        global_obj = GuardrailGlobals()
        global_obj.lint_ignore = None
        global_obj.pylintrc = None
        returnval = global_obj.mutable_lint_cmd()
        self.assertEqual(returnval, "")

    def test_generate_pylint_cmd_string(self):
        """Function to test generate_pylint_cmd_string method"""
        import os
        global_obj = GuardrailGlobals()
        global_obj.linting = "random_linting_string"
        global_obj.python = "python"
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        ignore_file_path = os.path.join(ini_path, "test_resource", "pylint_ignore.txt")
        global_obj.lint_ignore = ignore_file_path
        global_obj.all_folders = "random_string"
        global_obj.mutable_lint_cmd = MagicMock(return_value="random_string")
        global_obj.generate_files_lint = MagicMock(return_value=" ")
        returnval = global_obj.generate_pylint_cmd()
        print(returnval)
        self.assertEqual(returnval[0], "python -m pylint    --output-format=parseable random_string")

    @staticmethod
    def refactor_test_get_exclude_empty(gate, string=None):
        """Function to test get_exclude_cc_empty method"""
        global_obj = GuardrailGlobals()
        retval = None
        if gate == "cc":
            global_obj.cyclo_exclude = string
            retval = global_obj.get_exclude_cc()
        if gate == "jscpd":
            global_obj.programming_language = string
            retval = global_obj.jscpd_format()
        if gate == "jscpd_ignore":
            global_obj.jscpd_ignore = string
            retval = global_obj.jscpd_ignore_file()
        if gate == "cov_rc":
            global_obj.covrc = string
            retval = global_obj.cov_rc_file()
        if gate == "deadcode":
            global_obj.dead_code_ignore = string
            retval = global_obj.dead_code_exclude()
        if gate == "mutation":
            global_obj.pylintrc = string
            retval = global_obj.mutable_lint_cmd()
        return retval

    def test_get_exclude_cc_empty(self):
        """Function to test get_exclude_cc_empty method"""
        self.assertEqual(self.refactor_test_get_exclude_empty(gate="cc"), "")

    def test_get_exclude_jscpd_empty(self):
        """Function to test get_exclude_jscpd_empty method"""
        self.assertEqual(self.refactor_test_get_exclude_empty(gate="jscpd"), "")

    def test_jscpd_ignore_file_empty(self):
        """Function to test jscpd_ignore_file_empty method"""
        self.assertEqual(self.refactor_test_get_exclude_empty(gate="jscpd_ignore"), "")

    def test_cov_rc_file_empty(self):
        """Function to test cov_rc_file_empty method"""
        self.assertEqual(self.refactor_test_get_exclude_empty(gate="cov_rc"), "")

    def test_dead_code_exclude_empty(self):
        """Function to test dead_code_exclude_empty method"""
        self.assertEqual(self.refactor_test_get_exclude_empty(gate="deadcode"), "")

    def test_get_exclude_cc_string(self):
        """Function to test get_exclude_cc_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("cc", "test, sample"), "-x test/* -x  sample/*")

    def test_get_exclude_jscpd_string(self):
        """Function to test get_exclude_jscpd_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("jscpd", "python"), '--format "python"')

    def test_jscpd_ignore_file_string(self):
        """Function to test jscpd_ignore_file_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("jscpd_ignore", "python"), '--ignore python')

    def test_cov_rc_file_string(self):
        """Function to test cov_rc_file_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("cov_rc", "None"), '--cov-config=None')

    def test_mutable_lint_cmd_string(self):
        """Function to test mutable_lint_cmd_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("mutation", "random_string"), " --rcfile random_string")

    def test_dead_code_exclude_string(self):
        """Function to test dead_code_exclude_string method"""
        self.assertEqual(self.refactor_test_get_exclude_empty("deadcode", "None"), '--exclude None')

    def test_init(self):
        """Function to test init method"""
        global_obj = GuardrailGlobals()
        self.assertEqual(global_obj.src_folder, None)
        self.assertEqual(global_obj.jscpd_root, None)
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
        self.assertEqual(global_obj.min_deadcode_confidence, 60)
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
        self.assertEqual(global_obj.lint_buffer, 20)

    def test_set_all(self):
        """Function to test set_all method"""
        import os
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        ini_path = os.path.join(ini_path, "test_resource", "guardrail.ini")
        global_obj = GuardrailGlobals()
        global_obj.set_all(ini_path, 30)
        self.assertEqual(global_obj.src_folder, "source_folder_input")
        self.assertEqual(global_obj.jscpd_root, "jscpd_root_input")
        self.assertEqual(global_obj.test_folder, "test_folder_input")
        self.assertEqual(global_obj.pytest, "pytest_root_input")
        self.assertEqual(global_obj.report_folder, "report_folder_input")
        self.assertEqual(global_obj.cyclo_exclude, "cyclomatic_complexity_exclude_input")
        self.assertEqual(global_obj.python, r"mypython")
        self.assertEqual(global_obj.pylintrc, "pylint_rc_file_input")
        self.assertEqual(global_obj.covrc, "coverage_rc_file_input")
        self.assertEqual(global_obj.dup_token, 20)
        self.assertEqual(global_obj.percent_cov, 85)
        self.assertEqual(global_obj.allow_dup, 5)
        self.assertEqual(global_obj.cc_limit, 10)
        self.assertEqual(global_obj.min_deadcode_confidence, 100)
        self.assertEqual(global_obj.allow_mutants, 30)
        self.assertEqual(global_obj.all_folders, "source_folder_input test_folder_input")
        self.assertEqual(global_obj.linting, True)
        self.assertEqual(global_obj.cpd, True)
        self.assertEqual(global_obj.cov, True)
        self.assertEqual(global_obj.mutation, True)
        self.assertEqual(global_obj.deadcode, True)
        self.assertEqual(global_obj.cycloc, True)
        self.assertEqual(global_obj.lint_ignore, "pylint_ignore_input")
        self.assertEqual(global_obj.programming_language, "python, java")
        self.assertEqual(global_obj.jscpd_ignore, "jscpd_ignore_input")
        self.assertEqual(global_obj.dead_code_ignore, "dead_code_ignore_input")
        self.assertEqual(global_obj.lint_buffer, 30)


if __name__ == '__main__':
    unittest.main()
