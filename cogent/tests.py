import unittest


class TestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.start_time = None
        self.stop_time = None
