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

import unittest
from datetime import datetime

from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.stream import AggregationFunction


class TestAnomalyResult(unittest.TestCase):

    LOWER = -10
    UPPER = 10
    PROBABILITY = 0.99
    IS_ANOMALY = True

    def get_instance(self):
        return AnomalyResult(self.LOWER, self.UPPER,
                             self.PROBABILITY, self.IS_ANOMALY)

    def test_constructor(self):
        anom_res = self.get_instance()
        self.assertEqual(anom_res.value_lower_limit, self.LOWER)
        self.assertEqual(anom_res.value_upper_limit, self.UPPER)
        self.assertEqual(anom_res.anomaly_probability, self.PROBABILITY)
        self.assertEqual(anom_res.is_anomaly, self.IS_ANOMALY)

    def test_to_dict(self):
        anom_res = self.get_instance()
        expected = {
            "value_lower_limit": self.LOWER,
            "value_upper_limit": self.UPPER,
            "anomaly_probability": self.PROBABILITY,
            "is_anomaly": self.IS_ANOMALY
        }
        self.assertDictEqual(anom_res.to_dict(), expected)


class TestOutputMessage(unittest.TestCase):

    APP = "app"
    AGG_WINDOW_MILLIS = 30000
    AGG_FUNCTION = AggregationFunction.AVG
    AGG_VALUE = 10
    TS = datetime.now()

    def get_instance(self):
        anom_res = TestAnomalyResult().get_instance()
        return OutputMessage(self.APP, anom_res, self.AGG_WINDOW_MILLIS,
                             self.AGG_FUNCTION, self.AGG_VALUE, self.TS)

    def test_constructor(self):
        out_msg = self.get_instance()
        self.assertEqual(out_msg.application, self.APP)
        self.assertEqual(out_msg.anomaly_results,
                         TestAnomalyResult().get_instance())
        self.assertEqual(out_msg.agg_function, self.AGG_FUNCTION)
        self.assertEqual(out_msg.agg_window_millis, self.AGG_WINDOW_MILLIS)
        self.assertEqual(out_msg.agg_value, self.AGG_VALUE)
        self.assertEqual(out_msg.ts, self.TS)
