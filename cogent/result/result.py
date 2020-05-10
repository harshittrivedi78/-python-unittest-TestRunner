import sys
import unittest
import datetime
from io import StringIO


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


class TestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=verbosity)
        self.success_count, self.error_count, self.fail_count, self.skip_count = 0, 0, 0, 0
        self.output_buffer = StringIO()
        self.result = []
        self.stdout0 = None
        self.stderr0 = None

    def startTest(self, test):
        test.start_time = datetime.datetime.now()
        super().startTest(test)
        self.output_buffer = StringIO()
        stdout_redirector.fp = self.output_buffer
        stderr_redirector.fp = self.output_buffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def _get_output(self):
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.output_buffer.getvalue()

    def _set_test_attributes(self, test, test_result, err=None, reason=None):
        test.result = test_result
        test.output = self._get_output()
        test.traceback = self._exc_info_to_string(err, test) if err else None
        test.reason = reason
        self.result.append(test)

    def stopTest(self, test):
        super().stopTest(test)
        test.stop_time = datetime.datetime.now()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        self._set_test_attributes(test, "success")

    def addError(self, test, err):
        self.error_count += 1
        super().addError(test, err)
        self._set_test_attributes(test, "error", err)

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        self._set_test_attributes(test, "skip", reason=reason)

    def addFailure(self, test, err):
        self.fail_count += 1
        super().addFailure(test, err)
        self._set_test_attributes(test, "fail", err)
