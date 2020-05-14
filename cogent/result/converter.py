import json
from dicttoxml import dicttoxml
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader


class BaseConverter:
    settings = None
    filename = None

    def save_as_file(self, result):
        assert self.__class__.filename is not None
        if self.filename:
            with open(self.filename, 'w') as file:
                file.write(result)

    def _set_filename(self, filename):
        self.__class__.filename = filename

    def convert(self, result, settings=None):
        self.__class__.settings = settings
        if settings.DEFAULT_CONVERTER == "HTML":
            self._set_filename(settings.HTML_TEST_REPORT_FILENAME)
            return html_converter.convert(result)
        elif settings.DEFAULT_CONVERTER == "JSON":
            self._set_filename(settings.JSON_TEST_REPORT_FILENAME)
            return json_converter.convert(result)
        elif settings.DEFAULT_CONVERTER == "XML":
            self._set_filename(settings.XML_TEST_REPORT_FILENAME)
            return xml_converter.convert(result)
        else:
            raise ValueError(
                "Converter: %s is not defined. Possible values are HTML, JSON and XML." % settings.DEFAULT_CONVERTER)


base_converter = BaseConverter()


class JsonConverter(BaseConverter):

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

    def convert(self, result):
        result = dicttoxml(result)
        return result


xml_converter = XMLConverter()


class HTMLConverter(BaseConverter):

    def setup_jinja_env(self):
        self.jinja_env = Environment(loader=FileSystemLoader(self.settings.STATIC_DIR),
                                     trim_blocks=True, lstrip_blocks=True)

    def render_base_html(self, report):
        return self.jinja_env.get_template('base.html').render(
            title=self.settings.PROJECT_NAME,
            report=report,
        )

    def convert(self, report, save_as_file=True):
        self.setup_jinja_env()
        result = self.render_base_html(report)
        self.save_as_file(result)
        return result


html_converter = HTMLConverter()
