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
    settings = None

    def run(self, test):
        assert self.__class__.settings is not None
        start_time = datetime.datetime.now()
        result = super().run(test)
        stop_time = datetime.datetime.now()
        TestReport.settings = self.__class__.settings
        report = TestReport.generate(result, start_time, stop_time)
        report = deserialize(report)
        base_converter.convert(report, self.__class__.settings)
        return result  # we need to return result here as unittest expect wasSuccessful() func in result obj.
