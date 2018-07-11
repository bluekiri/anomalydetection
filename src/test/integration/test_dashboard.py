# -*- coding:utf-8 -*- #
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
from datetime import datetime, timedelta

from tornado.testing import AsyncHTTPTestCase

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.core.config import Config
from anomalydetection.common.logging import LoggingMixin
from anomalydetection.dashboard.dashboard import make_app
from test import TEST_PATH


class TestDashboard(AsyncHTTPTestCase, LoggingMixin):

    headers = {}
    config = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = Config(
            "test",
            open("{}/anomdec-test.yml".format(TEST_PATH)))

        conf = cls.config.get_as_dict()
        repository = conf["test"][3][0].repository
        repository.initialize()

        anom = AnomalyResult(-1, 1, 0.5, False)
        ini_ts = datetime.now() - timedelta(days=1)
        for i in range(200):
            repository.insert(
                OutputMessage("app", anom, 1, AggregationFunction.NONE,
                              1, ts=ini_ts + timedelta(minutes=1)))

    @classmethod
    def tearDownClass(cls):
        conf = cls.config.get_as_dict()
        repository = conf["test"][3][0].repository
        os.remove(repository.conn_string)

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
        self.assertEqual(response.code, 404)
