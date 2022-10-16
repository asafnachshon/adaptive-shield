import tornado.web

from abc import ABCMeta
from bson import json_util
from http import HTTPStatus
from typing import Dict


class MainHandler(tornado.web.RequestHandler, metaclass=ABCMeta):
    http_status = HTTPStatus
    parameters: Dict
    request_args: Dict

    @classmethod
    def initialize(cls, **kwargs):
        pass

    async def prepare(self):
        self.parameters = {
            "parameter": self.get_argument(
                name="parameter",
                default=None,
            ),
        }
        self.request_args = {
            "body": json_util.loads(self.request.body) if self.request.body else {},
            "headers": {**self.request.headers},
            "path": self.request.path,
            "method": self.request.method,
        }

    def write_error(self, *args, **kwargs):
        self.set_status(args[0])
        self.finish(chunk=str(kwargs["exc_info"][1]))

    def log_exception(self, typ, value, tb):
        pass


__all__ = ["MainHandler"]
