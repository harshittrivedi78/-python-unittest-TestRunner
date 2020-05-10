import unittest
import datetime
from cogent.result.result import TestResult
from cogent.result.report import TestReport
# from cogent.result.converter import xml_converter


class TestRunner(unittest.TextTestRunner):
    resultclass = TestResult

    def run(self, test):
        start_time = datetime.datetime.now()
        result = super().run(test)
        stop_time = datetime.datetime.now()
        report = TestReport.generate(result, start_time, stop_time)
        return report
