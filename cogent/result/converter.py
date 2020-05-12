import json
from dicttoxml import dicttoxml
from collections import namedtuple
from cogent.settings import *
from jinja2 import Environment, FileSystemLoader


class BaseConverter:
    filename = None

    def save_as_file(self, result):
        if self.filename:
            with open(self.filename, 'w') as file:
                file.write(result)

    def convert(self, result):
        if DEFAULT_CONVERTER == "HTML":
            return html_converter.convert(result)
        elif DEFAULT_CONVERTER == "JSON":
            return json_converter.convert(result)
        elif DEFAULT_CONVERTER == "XML":
            return xml_converter.convert(result)
        else:
            raise ValueError(
                "Converter: %s is not defined. Possible values are HTML, JSON and XML." % DEFAULT_CONVERTER)


base_converter = BaseConverter()


class JsonConverter(BaseConverter):
    filename = JSON_TEST_REPORT_FILENAME

    def serialize(self):
        pass

    def deserialize(self, result):
        data = json.loads(result,
                          object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return data

    def convert(self, result, deserialize=False):
        result = json.dumps(result)
        if deserialize:
            return self.deserialize(result)
        return result


json_converter = JsonConverter()


class XMLConverter(BaseConverter):
    filename = XML_TEST_REPORT_FILENAME

    def convert(self, result):
        result = dicttoxml(result)
        return result


xml_converter = XMLConverter()


class HTMLConverter(BaseConverter):
    filename = HTML_TEST_REPORT_FILENAME

    def __init__(self):
        self.jinja_env = Environment(loader=FileSystemLoader(STATIC_DIR),
                                     trim_blocks=True, lstrip_blocks=True)

    def render_base_html(self, report):
        return self.jinja_env.get_template('base.html').render(
            title=HTML_REPORT_TITLE,
            report=report,
        )

    def convert(self, report, save_as_file=True):
        result = self.render_base_html(report)
        self.save_as_file(result)
        return result


html_converter = HTMLConverter()
