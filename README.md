## python-unittest-cogent
A custom tests runner which gives output in three different formats (xml, json and html).

### Quickstart
Installation:
```shell
pip install python-unittest-cogent
```
Usage: In example.py
```python
import cogent
from cogent.tests import TestCase

class TestClassOne(TestCase):
    def test1(self):
        expected_number = 90
        actual_number = 90
        print('Test output foe test case 1')
        self.assertEqual(expected_number, actual_number)

if __name__ == "__main__":
    cogent.main()
```

### To change the output format:


#Install TestRunner -
You can install this runner into you system by using its setup.py file.you can do this as -
-- By download the zip file and then extract it and then open command line ( python setup.py install)

#How to use?

There is two unittest classes as TestClassOne and TestClassTwo and then I created a main method in which I do create a test suite and run the suite using this TestRunner.run() method:

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
        #Skipped Test Case
        pass
        
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
        
    if __name__ == '__main__':
        test_classes_to_run = [ TestClassOne  , TestClassTwo]
        suites_list = []
        dirName = TestRunner.create_result_hierarchy(projectname ='Test Project')
        for test_class in test_classes_to_run:
            itersuite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            suites_list.append(itersuite)
        big_suite = unittest.TestSuite(suites_list)
        result = TestRunner().run(test = big_suite , filepath = dirName , filename = 'result' , result_type = ResultType.ALL ,converter = r'Full Path of NunitHTMLReportGenerator.exe file' , app_version = '0.0.4')

#Explain Above Code

Method 'create_result_hierarchy' is implemented to create the directories into your system's document folder as per your project name then by date then by time and will store your result files into this direcotry such as - \Documents\Test Project\2015-01-31\23-49-29 . All result files will store here. you can define your as well by not using this method and pass the path in 'run' method in param 'filepath'.

Method 'run' is basically use to run the test suite or any test module . It has some params such as -
'test' : Positional argument which is must be given. It can be either a suite or a module or a class which is to be tested.
'filepath' : Positional argument which is must be given . It is basically the location where you want to store your result files.
'filename' : Optional argument. Default value is 'result' . This is the name which you want to see as your resulted file name.
'result_type' : Optional argument . It is Enum. Default Value is ResultType.XML . If you want only JSON file just say ResultType.JSON , in case only html file then just say ResultType.JSON similarily ResultType.HTML . In case for all three formats just say ResultType.ALL .

'converter' : Optional argument. Default Value is None. If you have requested for HTML result file then you must provide with this converter filepath to generate the HTML result. In case you say ResultType.HTML and do not provide the converter filepath then code will raise an error.

app_version : It is aslo an Optional argument. Default Value is '0.0.0' . It will showing you on your result files.

In case any queries you can contact me at my email - harshittrivedi78@gmail.com
