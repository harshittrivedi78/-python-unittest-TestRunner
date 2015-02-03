'''
Created on Jan 8, 2015

@author: Harshit
'''

#########################################################################################################################
#########################################################################################################################
'''
Wrapper to redirect stdout and stderr. 
'''

import datetime
from io import StringIO
import os
import sys
import time
import unittest
from xml.sax import saxutils

import TestRunner.html_generator
from TestRunner.json_generator import serialize
from TestRunner.result_types import ResultType
from TestRunner.xml_generator import Generate , SaveAs


class OutputRedirector(object):
    
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

#####################################################################################

'''
Initialize the unittest.TestResult with my custom variable.
'''
TestResult = unittest.TestResult


'''
Note: _TestResult is a pure representation of results.
It lacks the output and reporting ability compares to unittest._TextTestResult.
'''

class _TestResult(TestResult):
    
    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.outputBuffer = StringIO()
        self.result = []


    def startTest(self, test):
        TestResult.startTest(self, test)
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        '''
          Usually one of addSuccess, addError or addFailure would have been called.
          But there are some path in unittest that would bypass this.
          We must disconnect stdout in stopTest(), which is guaranteed to be called.
        '''
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


######################################################################################################

class TestRunner():
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        
    def run(self, test , filepath , filename = 'result' , result_type = ResultType.XML , converter = None , app_version = '0.0.0'):
        "Run the given test case or test suite."
        # By Default it will generate two formatted files - Json and Xml.
        '''
        @params:
        filepath - This is the path for putting up the result files.
        converter - This is the path of your NUnitHTMLReportGenerator.exe . If not given then html formatted file will not be generated.
        result_file_name - it the name what you want to see of your result files. By default it 'result'. Don't mention the format of the files.
        you are restricted to say your filename as result.html or result.xml . jsut say result without any extension.
        '''
        try:
            self.startTime = datetime.datetime.now()
            result = _TestResult(1)
            test(result)
            self.stopTime = datetime.datetime.now()
            output = self.generateReport(test, result)
            if result_type == ResultType.JSON:
                SaveAs(filepath , '{0}.json'.format(filename) , output)
            elif result_type == ResultType.XML:
                xml_output = Generate(serialize(output))
                xml_filepath = filepath + "\\{0}.xml".format(filename)
                SaveAs(filepath , '{0}.xml'.format(filename) , xml_output)
            elif result_type == ResultType.HTML:
                xml_output = Generate(serialize(output))
                xml_filepath = filepath + "\\{0}.xml".format(filename)
                SaveAs(filepath , '{0}.xml'.format(filename) , xml_output)
                html_generator.Generate(converter, xml_filepath, filepath, '{0}.html'.format(filename))
            elif result_type == ResultType.ALL:
                SaveAs(filepath , '{0}.json'.format(filename) , output)
                xml_output = Generate(serialize(output))
                xml_filepath = filepath + "\\{0}.xml".format(filename)
                SaveAs(filepath , '{0}.xml'.format(filename) , xml_output)
                SaveAs(filepath , '{0}.xml'.format(filename) , xml_output)
                html_generator.Generate(converter, xml_filepath, filepath, '{0}.html'.format(filename) ,  keep_xml = True)
            else:
                print("No any file can be generated.")
            return serialize(output)
        except Exception as ex:
            print(ex)
    
    @staticmethod
    def create_result_hierarchy(projectname = 'Test Project'):
        '''
           @params:
           projectname is the argument which is to passed in this method . It will create a folder in
           documents directory and then create a folder for today and inside this a folder for that perticular time
           instance. All the results will be saving into this folder.
           
        '''
        from time import gmtime, strftime
        userhome = os.path.expanduser('~')
        Documents = userhome + '\\Documents'
        Test_folder = Documents + "\\" +projectname
        if os.path.exists(Test_folder) == False:
            os.mkdir(Test_folder)
        result_folder = Test_folder + "\\" + strftime("%Y-%m-%d", gmtime())
        if os.path.exists(result_folder) == False:
            os.mkdir(result_folder)
        result_files_folder = result_folder + "\\" + time.strftime('%H-%M-%S')
        if os.path.exists(result_files_folder) == False:
            os.mkdir(result_files_folder)
        return result_files_folder
    
    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r
    
    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        report = self._generate_report(result)
        output = dict(
            report = report,
            reportattributes = report_attrs
        )
        return output
        
        
    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        stoptime = str(self.stopTime)[:19]
        duration = str(self.stopTime - self.startTime)
        
        if result.success_count: passed =  result.success_count
        if result.failure_count: failed = result.failure_count
        if result.error_count:   error  =  result.error_count  
        if len(result.skipped) > 0: skipped = len(result.skipped)
        
        total = passed + failed + error + skipped
        
        return dict( start_time = startTime , stop_time = stoptime , duration = duration , success = passed , fail = failed , 
                     error = error , skip = skipped , total = total)
        
    def _generate_report(self, result):
        rows = []
        test_rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n,t,o,e in cls_results:
                if n == 0: np += 1
                elif n == 1: nf += 1
                else: ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row =  dict(
                result = ne > 0 and 'error' or nf > 0 and 'fail' or 'pass',
                desc = desc,
                total = np+nf+ne,
                success = np,
                fail = nf,
                error = ne,
                cid = (cid+1),
                tests = []
            )
            rows.append(row)
            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(test_rows, cid, tid, n, t, o, e)
                
        skipped_result = self._get_skipped_test_report(result)
        for item in skipped_result:
            test_rows.append(item)
        for item in rows:
            for test_item in test_rows:
                if item['cid'] == test_item['cid']:
                    item['tests'].append(test_item)
        return rows

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        #tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid+1,tid+1)
        tid = tid+1
        cid = cid + 1
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = o
        else:
            uo = o.decode('latin-1')
           
        if isinstance(e,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            ue = e
        else:
            ue = e.decode('latin-1')
            
        if n== 0: result = 'pass'
        elif n == 1: result = 'fail' 
        else: result = 'error'

        row = dict(
            tid = tid,
            cid = cid,
            result = result,
            desc = desc,
            executed = True,
            output = saxutils.escape(uo+ue).replace('''"''' ,'')
        )
        rows.append(row)
        
        
    def _get_skipped_test_report(self , result):
        r = []
        id = 1
        if len(result.skipped) > 0:
            for item in result.skipped:
                skipped_result = {}
                value = str(item[0])
                skipped_result['desc'] = value[:value.find('(')].rstrip()
                skipped_result['skip'] = True
                skipped_result['cid'] = id
                skipped_result['tid'] = 0
                skipped_result['result'] = 'skip'
                skipped_result['output'] = ''
                skipped_result['executed']  = False
                r.append(skipped_result)
                id += 1
        return r
                    
   
###############################################################################################
