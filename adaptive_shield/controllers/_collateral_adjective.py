import os

from abc import ABCMeta
from adaptive_shield.controllers import MainHandler
from adaptive_shield.errors import LoadDataFromFileError
from adaptive_shield.utils import load_data_from_file


class CollateralAdjective(MainHandler, metaclass=ABCMeta):
    pattern = r"/animals/collateral-adjective"

    async def get(self):
        try:
            response = load_data_from_file(
                file_path=os.getenv("LOCAL_COLLATERAL_ADJECTIVE_HTML")
            )
            self.set_status(self.http_status.OK)
            await self.finish(chunk=response)

        except LoadDataFromFileError:
            self.set_status(self.http_status.NOT_FOUND)
            await self.finish(chunk="collateral adjective data not found, try again later")


__all__ = ["CollateralAdjective"]
