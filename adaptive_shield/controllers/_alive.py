from abc import ABCMeta
from adaptive_shield.controllers import MainHandler


class Alive(MainHandler, metaclass=ABCMeta):
    pattern = r"/alive"

    async def get(self):
        response = "Service is alive!"
        self.set_status(self.http_status.OK)
        await self.finish(chunk=response)


__all__ = ["Alive"]
