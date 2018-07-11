# -*- coding: utf-8 -*-
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from anomalydetection.backend.core.config import Config
from anomalydetection.dashboard.settings import settings


def make_app(kwargs):
    from anomalydetection.dashboard.urls import urls
    return Application(urls, **kwargs)


def main(callables: list, config: Config):
    settings.update({"config": config})
    app = make_app(settings)
    port = os.getenv("PORT", "5000")
    server = HTTPServer(app)
    ioloop = IOLoop.current()

    # Run async in executor
    for func in callables:
        ioloop.run_in_executor(None, func, config)

    server.listen(int(port))
    server.start()
    ioloop.start()


if __name__ == '__main__':
    main(callables=[], config=Config())
