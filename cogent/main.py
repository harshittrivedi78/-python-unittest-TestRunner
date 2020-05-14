import unittest
from cogent.runner import TestRunner
from cogent import settings


class TestProgram(unittest.TestProgram):
    settings = settings

    def runTests(self):
        TestRunner.settings = self.__class__.settings
        self.testRunner = TestRunner
        super().runTests()


main = TestProgram
