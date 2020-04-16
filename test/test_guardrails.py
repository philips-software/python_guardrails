""" This file does the  test of the guardrails """
import subprocess
import unittest
import xml.etree.ElementTree as ETree
from unittest import mock
from unittest.mock import patch, Mock
from guardrails.guardrail_globals import GuardrailGlobals
from guardrails.guardrails import Guardails


class TestGuardrails(unittest.TestCase):
    """ Class to test the guardrails """

    def tearDown(self):
        """"Deletes the log files created."""
        import os
        ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        file_name = os.path.join(ini_path, "guardrails", "guardrails.log")
        if os.path.exists(file_name):
            open(file_name, 'w').close()

    @staticmethod
    def stub_globals(guardails_obj):
        """Function to stub all globals"""
        guardails_obj.src_folder = "abc"
        guardails_obj.test_folder = "test"
        guardails_obj.pytest = "abc"
        guardails_obj.report_folder = "abc/report"
        guardails_obj.cyclo_exclude = "abc/None"
        guardails_obj.python = "python"
        guardails_obj.pylintrc = ".pylintrc"
        guardails_obj.covrc = ".cov"
        guardails_obj.dup_token = 10
        guardails_obj.percent_cov = 80
        guardails_obj.allow_dup = 20
        guardails_obj.cc_limit = 10
        guardails_obj.allow_mutants = 10
        guardails_obj.all_folders = guardails_obj.src_folder + " " + guardails_obj.test_folder
        guardails_obj.linting = True
        guardails_obj.cpd = True
        guardails_obj.cov = True
        guardails_obj.mutation = True
        guardails_obj.deadcode = True
        guardails_obj.cycloc = True
        guardails_obj.lint_ignore = "x"
        guardails_obj.programming_language = "java"
        guardails_obj.jscpd_ignore = "y"
        guardails_obj.dead_code_ignore = "z"

    def generate_pylint_cmd(self):  # pylint: disable=R0201
        """Function stubbed to return generate_pylint_cmd method return value"""
        return "xyz"

    def stub_validate_return(self, val, message, guardrail):  # pylint: disable=W0613,R0201
        """Function stubbed to return false"""
        return False

    def return_jscpd_false(self, val, message):  # pylint: disable=W0613,R0201
        """Function stubbed to set parse_jscpd_report_json method value to false"""
        return False

    @staticmethod
    def stub_get_all_func_cnn():
        """Function stubbed to return get_all_func_cnn function return value"""
        list_data = {
            'get_file_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:11': '3',
            'get_function_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:28': '7'}
        return list_data

    @staticmethod
    def get_guardrails_obj():
        """Function to create guardrails class object"""
        import os
        ini_path = os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), os.pardir))
        ini_path = os.path.join(ini_path, "test_resource", "guardrail.ini")
        return Guardails(ini_path)

    def test_list_to_str_folders(self):
        """Function to test list_to_str_folders method"""
        guardails_obj = self.get_guardrails_obj()
        self.stub_globals(guardails_obj)
        self.assertEqual(guardails_obj.list_to_str_folders(), "abc test")

    def test_file_exists_exit(self):  # pylint: disable=R0201
        """Function to test file_exists_exit method"""
        with patch('sys.exit') as exit_mock:
            Guardails.file_exists("abc")
            assert exit_mock.called

    def test_file_exists(self):
        """Function to test file_exists method"""
        import os
        GuardrailGlobals.generate_pylint_cmd = self.generate_pylint_cmd
        ini_path = os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), os.pardir))
        with patch('sys.exit') as exit_mock:
            Guardails.file_exists(ini_path)
            assert not exit_mock.called

    def test_call_subprocess_error(self):
        """Function to test call_subprocess_error method"""
        guardails_obj = self.get_guardrails_obj()
        try:
            ret_val = guardails_obj.call_subprocess("lshrs")
        except KeyError:
            pass
        self.assertEqual(ret_val, 1)

    def test_call_subprocess_noerror(self):
        """Function to test call_subprocess_noerror method"""
        guardails_obj = self.get_guardrails_obj()
        ret_val = guardails_obj.call_subprocess("dir")
        self.assertEqual(ret_val, 0)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_check_report_dir(self, mock_path_exists, mock_mkdir):
        """Function to test check_report_dir method"""
        guardails_obj = self.get_guardrails_obj()
        mock_path_exists.return_value = True
        mock_mkdir.return_value = False
        guardails_obj.check_report_dir()
        self.assertTrue(mock_mkdir.called)

    @mock.patch('subprocess.call')
    def test_guardrail_lint(self, mock_subproc_call):
        """Function to test guardrail_lint method"""
        guardails_obj = self.get_guardrails_obj()
        file_name = self.get_file_name("guardrails", "guardrails.log")
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_lint()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail , passed Linting." in str(line.decode('utf-8')))
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_lint()
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue("Guardrail , failed Linting." in str(line.decode('utf-8')))
            assert exit_mock
        self.assertTrue(mock_subproc_call.called)

    @staticmethod
    def get_file_name(folder_name, file_name):
        """Function to test file_name method"""
        import os
        ini_path = os.path.abspath(os.path.join
                                   (os.path.dirname(__file__), os.pardir))
        return os.path.join(ini_path, folder_name, file_name)

    def test_validate_return(self):
        """Function to test validate_return method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        with patch('sys.exit') as exit_mock:
            guardails_obj.validate_return(1, "test", True)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            log_data = str(line).split(" ", 2)[2][:-5]
            assert log_data == "Guardrail , failed test."

    def test_validate_return_success(self):
        """Function to test validate_return_success method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        with patch('sys.exit') as exit_mock:
            guardails_obj.validate_return(0, "test", False)
            assert not exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail task, passed test" in str(line))

    def test_check_pass_fail_success(self):
        """Function to test check_pass_fail_success method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        with patch('sys.exit') as exit_mock:
            guardails_obj.check_pass_fail(10, 100, 10)
            assert not exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail gating, passed mutation" in str(line))

    def test_check_pass_fail_failure(self):
        """Function to test check_pass_fail_failure method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        with patch('sys.exit') as exit_mock:
            guardails_obj.check_pass_fail(10, 100, 1)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail gating, failed mutation" in str(line))

    def test_check_pass_fail_failure_total(self):
        """Function to test check_pass_fail_failure_total method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        with patch('sys.exit') as exit_mock:
            guardails_obj.check_pass_fail(10, 0, 10)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail gating, failed: mutation test did not run" in str(line))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_jscpd(self, mock_subproc_call):
        """Function to test guardrail_jscpd method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = False
        guardails_obj.parse_jscpd_report_json = self.return_jscpd_false
        guardails_obj.guardrail_jscpd()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail task, passed Copy Paste Detection report generation" in str(line.decode('utf-8')))
        line = subprocess.check_output(['tail', '-2', file_name], shell=True)
        val = r'command for sub process:jscpd --min-tokens 20  --ignore C:\Projects\PythonRepo\python_sample' \
              r'\FunctionDefExtractor\test  --max-lines 100000 --max-size 100mb --reporters "json" --mode "strict" ' \
              r'--format "python, java" -o'
        self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_jscpd_fail(self, mock_subproc_call):
        """Function to test guardrail_jscpd_fail method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = True
        guardails_obj.parse_jscpd_report_json = self.return_jscpd_false
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_jscpd()
            self.assertTrue(mock_subproc_call.called)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail task, failed Copy Paste Detection report generation" in str(line.decode(
                'utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            val = r'command for sub process:jscpd --min-tokens 20  --ignore C:\Projects\PythonRepo\python_sample' \
                  r'\FunctionDefExtractor\test  --max-lines 100000 --max-size 100mb --reporters "json" --mode ' \
                  r'"strict" --format "python, java" -o'
            self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_test(self, mock_subproc_call):
        """Function to test guardrail_test method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_test()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail task, passed Test execution and coverage generation" in str(line.decode('utf-8')))
        line = subprocess.check_output(['tail', '-2', file_name], shell=True)
        val = r'mypython -m pytest C:\Projects\PythonRepo\python_sample\FunctionDefExtractor' \
              r' --cov-config=C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.coveragerc ' \
              r'--cov-report "html" --cov=C:\Projects\PythonRepo\python_sample' \
              r'\FunctionDefExtractor\functiondefextractor'
        self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_test_fail(self, mock_subproc_call):
        """Function to test guardrail_test_fail method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_test()
            self.assertTrue(mock_subproc_call.called)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail task, failed Test execution and coverage generation" in str(line.decode(
                'utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            val = r'mypython -m pytest C:\Projects\PythonRepo\python_sample\FunctionDefExtractor ' \
                  r'--cov-config=C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\.coveragerc ' \
                  r'--cov-report "html" --cov=C:\Projects\PythonRepo\python_sample' \
                  r'\FunctionDefExtractor\functiondefextractor'
            self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_coverage(self, mock_subproc_call):
        """Function to test guardrail_coverage method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_coverage()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail , passed Coverage threshold" in str(line.decode('utf-8')))
        line = subprocess.check_output(['tail', '-2', file_name], shell=True)
        val = r'mypython -m coverage report --fail-under=85'
        self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_coverage_fail(self, mock_subproc_call):
        """Function to test guardrail_coverage_fail method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_coverage()
            self.assertTrue(mock_subproc_call.called)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail , failed Coverage threshold" in str(line.decode(
                'utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            val = r'mypython -m coverage report --fail-under=85'
            self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_deadcode(self, mock_subproc_call):
        """Function to test guardrail_deadcode method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_deadcode()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail , passed Dead code detection" in str(line.decode('utf-8')))
        line = subprocess.check_output(['tail', '-2', file_name], shell=True)
        val = r'mypython -m vulture C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\functiondefextractor ' \
              r'C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test  --exclude C:\Projects\PythonRepo' \
              r'\python_sample\FunctionDefExtractor\test >C:\Projects\PythonRepo\REPORT\deadcode.txt'
        self.assertTrue(str(val) in str(line.decode('utf-8')))

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_deadcode_fail(self, mock_subproc_call):
        """Function to test guardrail_deadcode_fail method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_deadcode()
            self.assertTrue(mock_subproc_call.called)
            assert exit_mock.called
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail , failed Dead code detection" in str(line.decode(
                'utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            val = r'mypython -m vulture C:\Projects\PythonRepo\python_sample\FunctionDefExtractor' \
                  r'\functiondefextractor C:\Projects\PythonRepo\python_sample\FunctionDefExtractor' \
                  r'\test  --exclude C:\Projects\PythonRepo\python_sample\FunctionDefExtractor\test >C:' \
                  r'\Projects\PythonRepo\REPORT\deadcode.txt'
            self.assertTrue(str(val) in str(line.decode('utf-8')))

    def test_parse_jscpd_report_json(self):
        """Function to test parse_jscpd_report_json method"""
        guardails_obj = self.get_guardrails_obj()
        file_name = self.get_file_name("test_resource", "jscpd-report.json")
        guardails_obj.parse_jscpd_report_json(5, file_name)
        with patch('sys.exit') as exit_mock:
            guardails_obj.parse_jscpd_report_json(0, file_name)
            file_name = self.get_file_name("test_resource", "jscpd-report_test.json")
            guardails_obj.parse_jscpd_report_json(0, file_name)
            file_name = self.get_file_name("test_resource", "jscpd-report_test _error.json")
            guardails_obj.parse_jscpd_report_json(0, file_name)
            assert exit_mock.called
            file_name = self.get_file_name("guardrails", "guardrails.log")
            line = subprocess.check_output(['tail', '-3', file_name], shell=True)
            self.assertTrue("Guardrail gating, failed jscpd." in str(line.decode('utf-8')))
            line = subprocess.check_output(['tail', '-4', file_name], shell=True)
            self.assertTrue("Guardrail gating passed jscpd" in str(line.decode('utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue("jscpd report not correctly generated" in str(line.decode('utf-8')))
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("jscpd report not generated" in str(line.decode('utf-8')))

    def test_parse_cyclo_report_xml(self):
        """Function to test parse_cyclo_report_xml method"""
        file_name = self.get_file_name("test_resource", "CC.xml")
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.get_all_func_cnn = Mock()
        guardails_obj.get_all_func_cnn.return_value = self.stub_get_all_func_cnn
        assert guardails_obj.parse_cyclo_report_xml(file_name)
        file_name = self.get_file_name("test_resourc", "CC.xml")
        with patch('sys.exit') as exit_mock:
            guardails_obj.parse_cyclo_report_xml(file_name)
            file_name = self.get_file_name("test_resource", "CC_test.xml")
            guardails_obj.parse_cyclo_report_xml(file_name)
            file_name = self.get_file_name("test_resource", "CC_test_none.xml")
            guardails_obj.parse_cyclo_report_xml(file_name)
            assert exit_mock.called
            file_name = self.get_file_name("guardrails", "guardrails.log")
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("cc.xml report file path" in str(line.decode('utf-8')))
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue("tags required are not found in cc.xml report file path" in str(line.decode('utf-8')))

    def test_get_all_func_cnn(self):
        """Function to test get_all_func_cnn method"""
        file_name = self.get_file_name("test_resource", "CC.xml")
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.get_index_cnn = Mock()
        guardails_obj.get_index_cnn.return_value = int(2)
        expec_data = {
            'get_file_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:11': '3',
            'get_function_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:28': '7'}
        root = ETree.parse(file_name).getroot()
        for functions in root.iter('measure'):
            if functions.attrib['type'] == "Function":
                func_return_data = guardails_obj.get_all_func_cnn(functions)
        assert expec_data == func_return_data
        file_name = self.get_file_name("test_resource", "CC_test_Func.xml")
        root = ETree.parse(file_name).getroot()
        with patch('sys.exit') as exit_mock:
            for functions in root.iter('measure'):
                if functions.attrib['type'] == "Function":
                    guardails_obj.get_all_func_cnn(functions)
            file_name = self.get_file_name("test_resource", "CC_test_func_empty.xml")
            root = ETree.parse(file_name).getroot()
            for functions in root.iter('measure'):
                if functions.attrib['type'] == "Function":
                    guardails_obj.get_all_func_cnn(functions)
            assert exit_mock.called
            file_name = self.get_file_name("guardrails", "guardrails.log")
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue(
                "Guardrail unable to find the tags item/value/name in the report " in str(line.decode('utf-8')))
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue(
                "Guardrail unable to find the tags item/value/name in the report file " in str(line.decode('utf-8')))

    def test_get_index_cnn(self):
        """Function to test get_index_cnn method"""
        file_name = self.get_file_name("test_resource", "CC.xml")
        guardails_obj = self.get_guardrails_obj()
        root = ETree.parse(file_name).getroot()
        for functions in root.iter('measure'):
            if functions.attrib['type'] == "Function":
                func_return_data = guardails_obj.get_index_cnn(functions)
        assert func_return_data == 2
        file_name = self.get_file_name("test_resource", "CC_test_func_empty.xml")
        root = ETree.parse(file_name).getroot()
        with patch('sys.exit') as exit_mock:
            for functions in root.iter('measure'):
                if functions.attrib['type'] == "Function":
                    guardails_obj.get_index_cnn(functions)
            assert exit_mock.called
            file_name = self.get_file_name("guardrails", "guardrails.log")
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("Guardrail unable to find the tag CCN in the report " in str(line.decode('utf-8')))

    def test_parse_mutmut_report_xml(self):
        """Function to test parse_mutmut_report_xml method"""
        file_name = self.get_file_name("test_resource", "mutmut.xml")
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.parse_mutmut_report_xml(50, file_name)
        file_name = self.get_file_name("guardrails", "guardrails.log")
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail gating, passed mutation" in str(line))
        file_name = self.get_file_name("test_resourc", "mutmut.xml")
        with patch('sys.exit') as exit_mock:
            guardails_obj.parse_mutmut_report_xml(50, file_name)
            assert exit_mock.called
            file_name = self.get_file_name("guardrails", "guardrails.log")
            line = subprocess.check_output(['tail', '-1', file_name], shell=True)
            self.assertTrue("mutmut.xml report file path cound not be found" in str(line.decode('utf-8')))

    @mock.patch('subprocess.call')
    def test_guardrail_mutation(self, mock_subproc_call):
        """Function to test guardrail_mutation method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.parse_mutmut_report_xml = Mock()
        guardails_obj.parse_mutmut_report_xml.return_value = None
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_mutation()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail task, passed Mutation testing report generation." in str(line.decode('utf-8')))
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_mutation()
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue("Guardrail task, failed Mutation testing " in str(line.decode('utf-8')))
            assert exit_mock

    @mock.patch('subprocess.call', autospec=True)
    def test_guardrail_cyclomatic_complexity(self, mock_subproc_call):
        """Function to test guardrail_cyclomatic_complexity method"""
        file_name = self.get_file_name("guardrails", "guardrails.log")
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.parse_cyclo_report_xml = Mock()
        guardails_obj.parse_cyclo_report_xml.return_value = {
            'get_file_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:11': '3',
            'get_function_names(...) at C:\\Projects\\PythonRepo\\python_sample\\FunctionDefExtractor' \
            '\\functiondefextractor\\core_extractor.py:28': '7'}
        mock_subproc_call.return_value = False
        guardails_obj.guardrail_cyclomatic_complexity()
        self.assertTrue(mock_subproc_call.called)
        line = subprocess.check_output(['tail', '-1', file_name], shell=True)
        self.assertTrue("Guardrail , passed Cyclomatic complexity" in str(line.decode('utf-8')))
        mock_subproc_call.return_value = True
        with patch('sys.exit') as exit_mock:
            guardails_obj.guardrail_cyclomatic_complexity()
            line = subprocess.check_output(['tail', '-2', file_name], shell=True)
            self.assertTrue("Guardrail task, failed Cyclomating complexity generation" in str(line.decode('utf-8')))
            assert exit_mock

    @mock.patch('subprocess.call')
    @mock.patch('shutil.rmtree')
    @mock.patch('shutil.move')
    def test_mov_cov_report(self, mock_subproc_call, mock_shut_rmtr, mock_shut_mov):
        """Function to test mov_cov_report method"""
        guardails_obj = self.get_guardrails_obj()
        process_sub_mock = mock.Mock()
        patcher_exist = mock.patch('os.path.exists')
        mock_thing = patcher_exist.start()
        mock_thing.return_value = True
        patcher_isdir = mock.patch('os.path.isdir')
        mock_thing_isdir = patcher_isdir.start()
        mock_thing_isdir.return_value = True
        mock_subproc_call.return_value = process_sub_mock
        mock_shut_rmtr.return_value = process_sub_mock
        mock_shut_mov.return_value = process_sub_mock
        guardails_obj.validate_return = self.stub_validate_return
        guardails_obj.mov_cov_report()
        self.assertTrue(mock_subproc_call.called)

    def test_orchestrate_guardrails(self):
        """Function to test orchestrate_guardrails method"""
        guardails_obj = self.get_guardrails_obj()
        guardails_obj.check_report_dir = Mock()
        guardails_obj.mov_cov_report = Mock()
        guardails_obj.mov_cov_report.return_value = True
        self.assertTrue(guardails_obj.mov_cov_report.return_value)
        guardails_obj.guardrail_lint = Mock()
        guardails_obj.guardrail_lint.return_value = True
        self.assertTrue(guardails_obj.guardrail_lint.return_value)
        guardails_obj.guardrail_jscpd = Mock()
        guardails_obj.guardrail_jscpd.return_value = True
        self.assertTrue(guardails_obj.guardrail_jscpd.return_value)
        guardails_obj.guardrail_test = Mock()
        guardails_obj.guardrail_test.return_value = True
        self.assertTrue(guardails_obj.guardrail_test.return_value)
        guardails_obj.guardrail_coverage = Mock()
        guardails_obj.guardrail_coverage.return_value = True
        self.assertTrue(guardails_obj.guardrail_coverage.return_value)
        guardails_obj.guardrail_mutation = Mock()
        guardails_obj.guardrail_mutation.return_value = True
        self.assertTrue(guardails_obj.guardrail_mutation.return_value)
        guardails_obj.guardrail_deadcode = Mock()
        guardails_obj.guardrail_deadcode.return_value = True
        self.assertTrue(guardails_obj.guardrail_deadcode.return_value)
        guardails_obj.guardrail_cyclomatic_complexity = Mock()
        guardails_obj.guardrail_cyclomatic_complexity.return_value = True
        self.assertTrue(guardails_obj.guardrail_cyclomatic_complexity.return_value)
        guardails_obj.orchestrate_guardrails()


if __name__ == '__main__':
    unittest.main()
