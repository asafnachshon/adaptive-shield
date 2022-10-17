import logging
import os
import tornado.testing
import tornado.web

from adaptive_shield.controllers import CollateralAdjective
from adaptive_shield.errors import LoadDataFromFileError, LoadDataMissingFileError
from http import HTTPStatus
from unittest.mock import patch


class TestApiApplication(tornado.web.Application):
    def __init__(self, **kwargs):
        tornado.web.Application.__init__(
            self,
            handlers=[
                tornado.web.url(
                    pattern=CollateralAdjective.pattern,
                    handler=CollateralAdjective,
                    kwargs=kwargs,
                ),
            ],
            debug=False,
            autoreload=False,
        )


def setUpModule():
    logging.getLogger("tornado.access").disabled = True


def tearDownModule():
    pass


@patch("adaptive_shield.controllers._collateral_adjective.load_data_from_file")
class CollateralAdjectiveTest(tornado.testing.AsyncHTTPTestCase):
    local_collateral_adjective_html = "/path/to/file.html"
    mock_environment_variables = patch.dict(os.environ)

    def tearDown(self):
        self.mock_environment_variables.stop()

    def get_app(self):
        kwargs = {}
        return TestApiApplication(**kwargs)

    def test_collateral_adjective(self, load_data_from_file):
        mock_data_from_html_file = "mock data"
        self.mock_environment_variables.values = {
            "LOCAL_COLLATERAL_ADJECTIVE_HTML": self.local_collateral_adjective_html,
        }
        self.mock_environment_variables.start()

        load_data_from_file.return_value = mock_data_from_html_file
        resp = self.fetch(
            path="/animals/collateral-adjective",
            method="GET",
            allow_nonstandard_methods=True,
        )

        self.assertEqual(HTTPStatus.OK, resp.code)

        response = resp.body.decode("utf-8")
        self.assertIsInstance(response, str)
        self.assertEqual(mock_data_from_html_file, response)

        load_data_from_file.assert_called_once_with(
            file_path=self.local_collateral_adjective_html
        )

    def test_loading_data_from_file_missing_file_error(self, load_data_from_file):
        self.mock_environment_variables.values = {
            "LOCAL_COLLATERAL_ADJECTIVE_HTML": self.local_collateral_adjective_html,
        }
        self.mock_environment_variables.start()
        load_data_from_file.side_effect = LoadDataMissingFileError(
            path=self.local_collateral_adjective_html
        )

        resp = self.fetch(
            path="/animals/collateral-adjective",
            method="GET",
            allow_nonstandard_methods=True,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, resp.code)

        response = resp.body.decode("utf-8")
        self.assertIsInstance(response, str)
        self.assertEqual(
            "collateral adjective data processing is still in progress, try again later",
            response,
        )

        load_data_from_file.assert_called_once_with(
            file_path=self.local_collateral_adjective_html
        )

    def test_error_loading_data_from_file(self, load_data_from_file):
        load_data_from_file.side_effect = LoadDataFromFileError(error="mock error")

        resp = self.fetch(
            path="/animals/collateral-adjective",
            method="GET",
            allow_nonstandard_methods=True,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.code)

        response = resp.body.decode("utf-8")
        self.assertIsInstance(response, str)
        self.assertEqual("error in loading collateral adjective data", response)

        load_data_from_file.assert_called_once_with(file_path=None)


if __name__ == "__main__":
    tornado.testing.main()
