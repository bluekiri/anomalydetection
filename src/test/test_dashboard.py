# -*- coding:utf-8 -*- #
import os
from datetime import datetime, timedelta

from tornado.testing import AsyncHTTPTestCase

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.common.config import Config
from anomalydetection.dashboard.dashboard import make_app


class TestDashboard(AsyncHTTPTestCase):

    headers = {}

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        # Initialize config
        self.config = Config(
            "test",
            open(os.path.dirname(__file__) + "/anomdec-test.yml"))

    def setUp(self):
        super().setUp()

        conf = self.config.get_as_dict()

        repository = conf["test"][3][0].repository
        repository.initialize()

        anom = AnomalyResult(-1, 1, 0.5, False)
        ini_ts = datetime.now() - timedelta(days=1)
        for i in range(200):
            repository.insert(
                OutputMessage("app", anom, 1, "none",
                              1, ts=ini_ts + timedelta(minutes=1)))

        # Set cookie
        self.headers["Cookie"] = \
            "user=2|1:0|10:1528280738|4:user|16:YWRtaW4gLSBQT0Nz|33f8d9829628" \
            "65b4bc3d7dad42e0da78298b60e945351a3217672c7cfa7d07bb;session=2|1" \
            ":0|10:1528280738|7:session|48:YjhhMjVhYjEtZTQwMi00NmRmLWFlNWYtYT" \
            "YxMzY1YjgyZGNk|00f5dcf58b4899aa7dd9e6757941bc5e3cf777b45fcdc52b1" \
            "c8fb68ed7e45f2e"

    def get_app(self):
        from anomalydetection.dashboard.settings import settings
        settings.update({"config": self.config})
        return make_app(settings)

    def test_dashboard_homepage(self):
        response = self.fetch("/", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_homepage_reprocess_robust(self):
        response = self.fetch(
            "/?window=10&threshold=0.9999"
            "&engine=robust&application=app&name=test",
            method="GET", body=None, headers=self.headers)
        self.assertEqual(response.code, 200)

    def test_dashboard_homepage_reprocess_cad(self):
        response = self.fetch(
            "/?threshold=0.75"
            "&engine=cad&application=app&name=test",
            method="GET", body=None, headers=self.headers)
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
                              headers=self.headers,
                              max_redirects=1)
        print(response.body)
        self.assertEqual(response.code, 404)
