
import unittest
from runner_test.test_module_one import TestClassOne
from runner_test.test_module_two import TestClassTwo
from runner import TestRunner
from result_types import ResultType



if __name__ == '__main__':
    test_classes_to_run = [ TestClassOne  , TestClassTwo]
    suites_list = []
    dirName = TestRunner.create_result_hierarchy('Test Project')
    for test_class in test_classes_to_run:
        itersuite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suites_list.append(itersuite)
    big_suite = unittest.TestSuite(suites_list)
    result = TestRunner().run(big_suite , filepath = dirName , result_type = ResultType.ALL ,converter = r'C:\Users\Amit\Documents\Test Project\NunitHTMLReportGenerator.exe')
    

# TODO : delete converter.bat file
# TODO : delete result.xml file when I am just asking for Html formatted file.
