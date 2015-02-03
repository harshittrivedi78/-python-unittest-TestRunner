__author__ = 'Harshit'
__version__ = '5.3.0'


'''
XML-GENERATION MODULE
'''
import platform
import xml.dom.minidom
from xml.etree.ElementTree import tostring , Comment

from TestRunner.json_generator import deserialize
import xml.etree.ElementTree as ET


def Generate(json_response , project_name = "Test Project" , filepath = "" , app_version = "0.0.0"):
    json_object = deserialize(json_response)
    
    '''
    Root of the xml will have the information of overall result.
    '''
    root = ET.Element('test-results')
    root.append(Comment('Root of the xml will have the information of overall result.'))
    root.set('name' , project_name)
    root.set('total', str(json_object.reportattributes.total))
    root.set('success', str(json_object.reportattributes.success))
    root.set('errors', str(json_object.reportattributes.error))
    root.set('failures', str(json_object.reportattributes.fail))
    root.set('not-run',"0")
    root.set('inconclusive' , "0" )
    root.set('ignored' , "0")
    root.set('skipped' , str(json_object.reportattributes.skip))
    root.set('invalid' , "0")
    date = str(json_object.reportattributes.start_time)
    date = date[:date.find(" ")]
    root.set('date', date )
    time = json_object.reportattributes.duration
    root.set('time' , str(time[:time.find(".")]))
    
    
    '''
    Environment section will have the information about your system , your tested application version.
    '''
    # This is Environment section.
    root.append(Comment('Environment section will have the information about your system , your tested application version.'))
    environment = ET.SubElement(root, 'environment')
    environment.set('application-version',app_version)
    environment.set('platform', platform.platform())

    for item in json_object.report:
        test_suite = ET.SubElement(root, 'test-suite')
        test_suite.set('type' , "TestFixture")
        test_suite.set('name' , item.desc)
        test_suite.set('description' , "")
        test_suite.set('executed' , 'True')
        # result tag can have "Failure" , "Inconclusive" , "Success" ,"Skipped" , "Error"
        if item.result == 'error' or item.result == 'fail':
            test_suite.set('result' , "Failure")
        else:
            test_suite.set('result' , "Success")
        if item.error > 0 or item.fail > 0:
            test_suite.set('success' , 'False')
        else:
            test_suite.set('success' , 'True')
        test_suite.set("time" , "" )
        test_suite.set('asserts' , "0")
        results = ET.SubElement(test_suite, 'results')
        for test in item.tests:
            test_case = ET.SubElement(results, 'test-case')
            test_case.set('name' , test.desc)
            test_case.set('executed' , str(test.executed))
            # setting the attributes of the test case result as per json_generator result.
            if test.result == 'fail':
                test_case.set('result' , "Failure")
                test_case.set('success' , 'False')
            elif test.result == 'error':
                test_case.set('result' , "Error")
                test_case.set('success' , 'False')
            elif test.result == 'skip':
                test_case.set('result' , "Ignored")
                test_case.set('success' , 'False')
            else:
                test_case.set('result' , "Success")
                test_case.set('success' , 'True')
            test_case.set("time" , "" )
            test_case.set('asserts' , "0")
            # message is nothing just the print message behind you test cases. Separated buy '.' .
            # IF the reuslt is fail or error this must have a message as well as a Stack Trace .
            # So as a need conclude both and file it in xml string.
            if test.result == 'fail' or test.result == 'error':
                failure = ET.SubElement(test_case, 'failure')
                message = ET.SubElement(failure, 'message')
                message.text = "<![CDATA[{0}]]>".format(test.output[:test.output.find("Traceback")])
                stack_trace = ET.SubElement(failure, 'stack-trace')
                stack_trace.text = "<![CDATA[{0}]]>".format(test.output[test.output.find("Traceback"):])
            # IF the reuslt is pass this must have only a message.
            if test.result == 'pass':
                success = ET.SubElement(test_case, 'success')
                message = ET.SubElement(success, 'message')
                message.text = "<![CDATA[{0}]]>".format(test.output)

    # Convert the root in string by decoding this by utf-8 encoding style.        
    root = tostring(root).decode('utf-8')
    result = xml.dom.minidom.parseString(root)
    result = result.toprettyxml().replace("&lt;" ,"<")
    result = result.replace("&gt;" ,">")
    return result # return the xml string. you can either deserialize it also.


def SaveAs(filepath , filename , output):
    """
    @description: Save the file into filepath location with the filename as of filename arg and output is the string which you want to write
                  into this file.
                  
    @param filepath: Positional argument must be provided. This is the location where you are going to save your file.
    @param filename: Positional argument must be provided. This is the name of your file with which it will be saved. 
    @param output: Positional argument must be provided. This is the Output string which you want to write into your file.
    """
    with open(filepath + '\\' + filename , 'w') as f:
        f.write(str(output))
        f.close()
