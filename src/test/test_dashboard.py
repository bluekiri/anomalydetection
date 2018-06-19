# -*- coding:utf-8 -*- #
import os
from datetime import datetime, timedelta

from tornado.testing import AsyncHTTPTestCase

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.stream import AggregationFunction
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
                OutputMessage("app", anom, 1, AggregationFunction.NONE,
                              1, ts=ini_ts + timedelta(minutes=1)))

    def get_app(self):
        from anomalydetection.dashboard.settings import settings
        settings.update({"config": self.config})
        return make_app(settings)

    def test_dashboard_homepage(self):
        response = self.fetch("/", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_signal_list(self):
        response = self.fetch("/signals/", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_signal_test(self):
        response = self.fetch("/signals/test/", method="GET")
        self.assertEqual(response.code, 200)

    def test_dashboard_login(self):
        response = self.fetch("/login?next=%2F", method="POST",
                              body="username=admin&password=admin")

        self.assertEqual(response.code, 200)

    def test_dashboard_maintenance(self):
        response = self.fetch("/maintenance", method="GET", body=None)
        self.assertEqual(response.code, 200)

    def test_dashboard_404(self):
        response = self.fetch("/404/", method="GET", body=None)
        print(response.body)
        self.assertEqual(response.code, 404)
