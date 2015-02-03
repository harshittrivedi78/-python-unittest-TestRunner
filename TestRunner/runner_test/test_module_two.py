
import unittest

class TestClassTwo(unittest.TestCase):
    def test1(self):
        # Pass Test Case
        expected_number = 90
        actual_number = 90
        print('Test output foe test case 1')
        self.assertEqual(expected_number, actual_number)

    def test2(self):
        # Pass Test Case
        expected = True
        actual = True
        print('Test output foe test case 2')
        self.assertEqual(expected, actual)
        
        