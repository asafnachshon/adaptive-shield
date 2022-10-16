from bson import json_util
from json2html import json2html


def convert_object_to_html_table(obj):
    return json2html.convert(json_util.dumps(obj=obj))


__all__ = ["convert_object_to_html_table"]
