# -*- coding: utf-8 -*-

import os

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from anomalydetection.common.config import Config
from anomalydetection.dashboard.settings import settings


def make_app(kwargs):
    from anomalydetection.dashboard.urls import urls
    return Application(urls, **kwargs)


def main(callables=[], config: Config = Config()):
    settings.update({"config": config})
    app = make_app(settings)
    port = os.getenv("PORT", "5000")
    print("Server listening on port: %s" % port)
    server = HTTPServer(app)
    ioloop = IOLoop.current()

    for func in callables:
        ioloop.run_in_executor(None, func, config)

    server.listen(int(port))
    server.start()
    ioloop.start()


if __name__ == '__main__':
    main([], config=Config())
