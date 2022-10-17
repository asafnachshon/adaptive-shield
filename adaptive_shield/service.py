import os
import tornado.web

from adaptive_shield.controllers import Alive, CollateralAdjective
from adaptive_shield.scrapers import animals_by_collateral_adjective
from concurrent.futures import ProcessPoolExecutor
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import url


class Service(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(pattern=Alive.pattern, handler=Alive, kwargs={}),
            url(
                pattern=CollateralAdjective.pattern,
                handler=CollateralAdjective,
                kwargs={},
            ),
        ]
        tornado.web.Application.__init__(
            self, handlers=handlers, debug=False, autoreload=False
        )


__all__ = ["Service"]


def main():
    # run scrapers
    executor = ProcessPoolExecutor()
    executor.submit(animals_by_collateral_adjective)

    # start app
    app = Service()
    _tornado = HTTPServer(app)
    _tornado.bind(port=int(os.getenv("PORT")), address=os.getenv("ADDRESS"))
    _tornado.start(num_processes=int(os.getenv("THREADS")))
    IOLoop.current().start()


if __name__ == "__main__":
    main()
