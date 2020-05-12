import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_DIR = BASE_DIR + "/cogent/static/"

HTML_REPORT_TITLE = "Test Report"
APPLICATION_NAME = "Test APP"
APP_VERSION = "App Version 5.3"
PLATFORM = "Linux/Ubuntu 14.04"

HTML_TEST_REPORT_FILENAME = "Report.html"
XML_TEST_REPORT_FILENAME = "Report.xml"
JSON_TEST_REPORT_FILENAME = "Report.json"

DEFAULT_CONVERTER = "HTML"  # JSON, XML are the other types
