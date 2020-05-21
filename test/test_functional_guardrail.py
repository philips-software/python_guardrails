"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import shutil
import subprocess
import unittest
from shutil import copyfile

CURR_DIR = None


class TestGuardrailFunctional(unittest.TestCase):
    """ Class to test the functional flow of guardrails """

    def setUp(self):
        """"Sets the directory for the test case"""
        global CURR_DIR  # pylint: disable=W0603
        CURR_DIR = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def tearDown(self):
        """"Deletes the log files created."""
        global CURR_DIR  # pylint: disable=W0603
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        file_name = os.path.join(ini_path, "guardrails", "guardrails.log")
        if os.path.exists(file_name):
            open(file_name, 'w').close()
        file_name = os.path.join(ini_path, "test_resource", "sample_project", "sample_report")
        shutil.rmtree(file_name)
        os.chdir(CURR_DIR)

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_guardrail_functionality(self):  # pylint: disable=R0201
        """ Function to test the functional flow of guardrails"""
        ini_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "test_resource"))
        pylint_ignore = os.path.join(ini_path, "pylint_ignore.txt")
        ini_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "sample_project"))
        source_folder = os.path.join(ini_path, "source")
        test_folder = os.path.join(ini_path, "test")
        pytest_root = ini_path
        report_folder = os.path.join(ini_path, "sample_report")
        pylint_rc_file = os.path.join(ini_path, ".pylintrc")

        inifile = '''[folder]
        # Comma seperated source folders if more than one directory
        source_folder = {0}
        # Comma seperated test folders if more than one directory
        test_folder = {1}
        pytest_root = {2}
        report_folder = {3}
        jscpd_root = {6}

        [python]
        python = python
        # path to the .pylintrc file if specific linting or leave empty after =
        pylint_rc_file = {4}

        [coverage]
        # path to the .coveragerc file if specific cverage config or leave empty after =
        coverage_rc_file =

        [gates]
        # gate values are absolute integers
        # duplicate to ken count
        jscpd_duplicate_token = 20
        # Jscpd allowed % duplication
        jscpd_allowed_duplication = 5
        # coverage gating %
        coverage_percentage = 85
        # Allowed mutats %
        allowed_mutants_percentage = 20
        # cyclomatic complexity allowed value
        cyclomatic_complexity_allowed = 10
        # minimum deadcode confidence
        min_deadcode_confidence = 100
        
        [ignore]
        # Comma seperated folders if more than one directory or leave empty after =
        cyclomatic_complexity_exclude =
        # Comma seperated source folders if more than one directory or leave empty after =
        pylint_ignore = {5}
        # Comma seperated source folders if more than one directory or leave empty after =
        jscpd_ignore =
        # Comma seperated source folders if more than one directory or leave empty after =
        dead_code_ignore =
        [others]
        # Comma seperated language if more than one
        programming_language = python

        [options]
        # option can be either true or false
        linting=true
        cpd=true
        coverage=true
        mutation=false
        deadcode=true
        cyclomatic_complexity=true
        '''.format(source_folder, test_folder, pytest_root, report_folder, pylint_rc_file, pylint_ignore, ini_path)
        file_name = os.path.join(ini_path, "guardrail.ini")
        print(file_name)
        file_object = open(file_name, "w+")
        file_object.write(inifile)
        file_object.close()
        file_guardrails = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "guardrails", "guardrails.py"))
        file_ini = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "sample_project", "guardrail.ini"))
        cmd = "python {0} --p {1}".format(file_guardrails, file_ini)
        ini_path = os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), os.pardir))
        subprocess.call(cmd, shell=True)
        src = os.path.join(ini_path, "guardrails", "guardrails.log")
        dst = os.path.join(ini_path, "guardrails", "guardrail_test.log")
        copyfile(src, dst)
        base = os.path.splitext(dst)[0]
        os.rename(dst, base + '.txt')
        file_name = os.path.join(ini_path, "guardrails", "guardrail_test.txt")
        with open(file_name, 'r') as input_file:
            lines = input_file.readlines()
        open(file_name, 'w').close()
        start = 0
        stop = 23
        for line in lines:
            if len(line) > stop:
                line = line[0: start:] + line[stop + 1::]
                line = line.replace(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "$$$")
                with open(file_name, "a+") as input_file:
                    input_file.write(line)
        file_name = os.path.join(ini_path, "guardrails", "guardrail_test.txt")
        with open(file_name, 'r') as input_file:
            lines_test = input_file.readlines()
            lines_test.pop(2)
        os.remove(file_name)
        ini_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", "sample_project"))
        expec_file = os.path.join(ini_path, "test_guardrails.txt")
        with open(expec_file, 'r') as input_file:
            lines_expec = input_file.readlines()
        self.assertEqual(str(lines_expec).replace("\n", "").replace("\\", os.sep),
                         str(lines_test).replace("\n", "").replace("\\", os.sep))


if __name__ == '__main__':
    unittest.main()
