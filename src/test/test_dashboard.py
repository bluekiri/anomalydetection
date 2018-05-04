# -*- coding:utf-8 -*- #
import os
from datetime import datetime

from tornado.testing import AsyncHTTPTestCase

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from anomalydetection.dashboard.app import make_app

from test import config


class TestDashboard(AsyncHTTPTestCase):

    headers = {
       "Cookie": "session=2|1:0|10:1525430996|7:session|48:ODE5MjZkYTMtY"
                 "jVkMy00ZDNlLWFhNjktNjk5N2NlM2U0ZmFi|cb014ac5f4f81ef35d6"
                 "4b4af69edb3998eb6aca8e6ca2cfe3ced58787f2a6d31; user=2|1"
                 ":0|10:1525430996|4:user|16:YWRtaW4gLSBQT0Nz|ba7047c1a2a"
                 "6af09f7e8f0ca553ffbb35e11c4b0f694a661d9327159f30d312c"
    }

    def setUp(self):
        super().setUp()

        # Insert some data
        repository = SQLiteRepository(config["DATA_DB_FILE"])

        repository.initialize()
        anom = AnomalyResult(-1, 1, 0.5, False)
        repository.insert(OutputMessage("app", anom, 1, "none",
                                        1, ts=datetime.now()))
        repository.insert(OutputMessage("app", anom, 1, "none",
                                        1, ts=datetime.now()))
        repository.insert(OutputMessage("app", anom, 1, "none",
                                        1, ts=datetime.now()))
        repository.insert(OutputMessage("app", anom, 1, "none",
                                        1, ts=datetime.now()))

    def get_app(self):
        from anomalydetection.dashboard.settings import settings
        settings["conf"]["DATA_DB_FILE"] = config["DATA_DB_FILE"]
        return make_app(settings)

    def test_dashboard_homepage(self):
        response = self.fetch("/", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_homepage_reprocess(self):
        response = self.fetch("/?window=10&threshold=0.9999&engine=robust",
                              method="GET", body=None, headers=self.headers,
                              max_redirects=0)
        self.assertEqual(response.code, 200)

    def test_dashboard_login(self):
        response = self.fetch("/login?next=%2F", method="POST",
                              body="username=admin&password=admin",
                              max_redirects=0)

        self.assertEqual(response.code, 302)
        self.assertEqual(response.headers._dict['Location'], "/")

    def test_dashboard_maintenance(self):
        response = self.fetch("/maintenance", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_404(self):
        response = self.fetch("/404", method="GET", body=None,
                              headers=self.headers)
        self.assertEqual(response.code, 404)
