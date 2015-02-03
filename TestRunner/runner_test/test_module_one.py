
import unittest

class TestClassOne(unittest.TestCase):
    def test1(self):
        # Pass Test Case
        expected_number = 90
        actual_number = 90
        print('Test output foe test case 1')
        self.assertEqual(expected_number, actual_number)

    def test2(self):
        # Fail Test Case
        expected = True
        actual = False
        print('Test output foe test case 2')
        self.assertEqual(expected, actual)
        
    def test3(self):
        # Error Test Case
        print('Test output foe test case 3')
        raise ValueError('flowid not matches')
        

    @unittest.skip('skipped')
    def test4(self):
        # Skip Test Case
        pass
        