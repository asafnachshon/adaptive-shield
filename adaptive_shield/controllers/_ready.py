from abc import ABCMeta
from adaptive_shield.controllers import MainHandler


class Ready(MainHandler, metaclass=ABCMeta):
    pattern = r"/ready"

    async def get(self):
        response = "Service is ready!"
        self.set_status(self.http_status.OK)
        await self.finish(chunk=response)


__all__ = ["Ready"]
