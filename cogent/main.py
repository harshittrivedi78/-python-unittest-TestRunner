import unittest
from cogent.runner import TestRunner


class TestProgram(unittest.TestProgram):

    def runTests(self):
        self.testRunner = TestRunner
        super().runTests()


main = TestProgram
