# -*- coding: utf-8 -*-

import os

from tornado import ioloop
from tornado.web import Application

from anomalydetection.dashboard.urls import urls
from anomalydetection.dashboard.settings import settings


def make_app(kwargs):
    return Application(urls, **kwargs)


# Configure app with settings and urls
app = make_app(settings)

# Main, start server
if __name__ == '__main__':

    # Start server
    port = os.getenv("PORT", "5000")
    print("Server listening on port: %s" % port)
    app.listen(int(port))
    ioloop.IOLoop.current().start()
