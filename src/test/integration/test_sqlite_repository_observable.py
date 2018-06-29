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
import unittest
from datetime import datetime

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.common.logging import LoggingMixin


class SQLiteObservableRepository(unittest.TestCase, LoggingMixin):

    DB_FILE = "/tmp/test_sqlite_observable.sqlite"
    ANOM = AnomalyResult(-1, 1, 0.5, False)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repo = SQLiteRepository(cls.DB_FILE)
        cls.repo.initialize()
        cls.repo.insert(
            OutputMessage("app", cls.ANOM, 1, AggregationFunction.NONE,
                          1, ts=datetime.now()))
        cls.repo.insert(
            OutputMessage("app", cls.ANOM, 1, AggregationFunction.NONE,
                          4, ts=datetime.now()))
        cls.repo.insert(
            OutputMessage("app", cls.ANOM, 1, AggregationFunction.NONE,
                          3, ts=datetime.now()))
        cls.repo.insert(
            OutputMessage("app", cls.ANOM, 1, AggregationFunction.NONE,
                          2, ts=datetime.now()))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        os.remove(cls.DB_FILE)

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def test_observable_sqlite(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        obs_rep.get_observable() \
            .subscribe(lambda x: self.logger.debug(str(x)))

    def test_get_min(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        self.assertEqual(1, obs_rep.get_min())

    def test_get_max(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        self.assertEqual(4, obs_rep.get_max())
