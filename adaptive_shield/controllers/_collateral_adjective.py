import os

from abc import ABCMeta
from adaptive_shield.controllers import MainHandler
from adaptive_shield.errors import LoadDataFromFileError, LoadDataMissingFileError
from adaptive_shield.utils import load_data_from_file


class CollateralAdjective(MainHandler, metaclass=ABCMeta):
    pattern = r"/animals/collateral-adjective"

    async def get(self):
        try:
            # env variable `LOCAL_COLLATERAL_ADJECTIVE_HTML` is the key of the html file path (same is used in the
            # scraper).
            # the html content will return in this API response.
            response = load_data_from_file(
                file_path=os.getenv("LOCAL_COLLATERAL_ADJECTIVE_HTML")
            )
            self.set_status(self.http_status.OK)
            await self.finish(chunk=response)

        # if the file doesn't exist, data processing might be still in progress.
        # status code will be 400, but the API will return a massage saying the user should try again later.
        except LoadDataMissingFileError:
            self.set_status(self.http_status.NOT_FOUND)
            await self.finish(chunk="collateral adjective data processing is still in progress, try again later")

        # if local var 'LOCAL_COLLATERAL_ADJECTIVE_HTML' doesn't exist (None), or the value is not a path to a file (a
        # directory).
        # status code will be 404.
        except LoadDataFromFileError:
            self.set_status(self.http_status.BAD_REQUEST)
            await self.finish(chunk="error in loading collateral adjective data")


__all__ = ["CollateralAdjective"]
