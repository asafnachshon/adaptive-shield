import logging
import tornado.testing
import tornado.web

from http import HTTPStatus
from adaptive_shield.controllers import Ready


class TestApiApplication(tornado.web.Application):
    def __init__(self, **kwargs):
        kwargs = {**kwargs}

        tornado.web.Application.__init__(
            self,
            handlers=[
                tornado.web.url(pattern=Ready.pattern, handler=Ready, kwargs=kwargs),
            ],
            debug=False,
            autoreload=False,
        )


def setUpModule():
    logging.getLogger("tornado.access").disabled = True


def tearDownModule():
    pass


class ReadtTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        kwargs = {}
        return TestApiApplication(**kwargs)

    def test_alive(self):
        resp = self.fetch(path="/ready", method="GET")
        response = resp.body.decode("utf-8")
        self.assertEqual(HTTPStatus.OK, resp.code)
        self.assertEqual("Service is ready!", response)

    def test_alive_failure(self):
        resp = self.fetch(
            path="/ready", method="GET", body="body", allow_nonstandard_methods=True
        )
        response = resp.body.decode("utf-8")
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.code)
        self.assertIsInstance(response, str)
        self.assertEqual("Expecting value: line 1 column 1 (char 0)", response)


if __name__ == "__main__":
    tornado.testing.main()
