import unittest
import datetime
import json
from collections import namedtuple
from cogent.result.result import TestResult
from cogent.result.report import TestReport
from cogent.result.converter import base_converter


def deserialize(report):
    report = json.dumps(report)
    return json.loads(report, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


class TestRunner(unittest.TextTestRunner):
    resultclass = TestResult

    def run(self, test):
        start_time = datetime.datetime.now()
        result = super().run(test)
        stop_time = datetime.datetime.now()
        report = TestReport.generate(result, start_time, stop_time)
        report = deserialize(report)
        base_converter.convert(report)
        return result  # we need to return result here as unittest expect wasSuccessful() func in result obj.
