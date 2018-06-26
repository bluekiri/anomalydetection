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

from anomalydetection.backend.entities.output_message import AnomalyResult, OutputMessage
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from anomalydetection.backend.stream import AggregationFunction


class TestSQLiteRepository(unittest.TestCase):

    APP = "application"
    DB_FILE = "/tmp/anomalydetection.sqlite3"

    def setUp(self):
        super().setUp()
        self.repository = SQLiteRepository(self.DB_FILE)
        self.repository.initialize()

    def tearDown(self):
        super().tearDown()
        os.remove(self.DB_FILE)

    def test_constructor(self):
        self.assertEqual(self.repository.conn_string, self.DB_FILE)

    def test_insert_fetch_map(self):

        # Insert
        anom_results = AnomalyResult(-10, 10, 0.5, False)
        output_message = OutputMessage(self.APP, anom_results, 0,
                                       AggregationFunction.NONE,
                                       0, datetime(2018, 1, 1, 2, 0))
        self.repository.insert(output_message)

        # Fetch
        values = self.repository.fetch(self.APP,
                                       datetime(2018, 1, 1),
                                       datetime(2018, 1, 2))

        # Map
        output_messages = list(map(self.repository.map, values))
        self.assertDictEqual(output_message.to_dict(),
                             output_messages[0].to_dict())
