# -*- coding: utf-8 -*-

"""
File: app.py
Author: Cristòfol Torrens Morell <tofol.torrens@v5tech.es>
Description: Tour service
"""

import argparse

from tornado import ioloop
from tornado.web import Application

from anomalydetection.dashboard.urls import urls
from anomalydetection.dashboard.settings import settings

# Configure app with settings and urls
app = Application(urls, **settings)

# Main, start server
if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Dashboard")
    parser.add_argument("--listen", metavar="N", type=int,
                        help="Port to listen to.", default=8031)
    args = parser.parse_args()

    # Start server
    print("Server listening on port: %s" % args.listen)
    app.listen(args.listen)
    ioloop.IOLoop.current().start()
