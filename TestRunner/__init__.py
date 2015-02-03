# -*- coding: utf-8 -*-

# TEST RUNNER


"""
                     TestRunner library
                     ~~~~~~~~~~~~~~~~~~
                     
TestRunner is a python module which is basically a plug-in for python Unittest framework. 
It can provide you the result format as you want to have. Basically it has three types of result format which are - Xml, Json and 
much demanded Html. In case you want to get the output in HTML format then you will need to use NunitHTMLReportGenerator.exe file. 
I would like to explain the result generation technique of this module in brief. Basically when you execute your test suite or 
test module with its run method it returns the serialized JSON string and then I convert this JSON into a XML string and write 
it into a file then I do create a batch file named converter.bat and with the help of NunitHTMLReportGenerator.exe I do convert 
the XML file into a HTML file.


LICENESE - 


Copyright 2015 Harshit Trivedi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


"""


__name__ = "Test Runner"
__email__ = "harshittrivedi78@gmail.com"
__url__ = "https://github.com/"
__title__ = 'Test Result Generator'
__version__ = '5.3.0'
__build__ = 0x050300
__author__ = 'Harshit'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 Apache 2.0'
