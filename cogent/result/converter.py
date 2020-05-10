import json
from dicttoxml import dicttoxml


class BaseConverter:

    def convert(self, result):
        raise NotImplementedError


class JsonConverter(BaseConverter):

    def convert(self, result):
        result = json.dumps(result)
        return result


class XMLConverter(BaseConverter):

    def convert(self, result):
        result = dicttoxml(result)
        return result


xml_converter = XMLConverter()


class HTMLConverter(BaseConverter):

    def convert(self, result):
        result = result
        return result
