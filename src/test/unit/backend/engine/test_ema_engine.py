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

import random
import unittest
from datetime import timedelta, datetime

import numpy as np

from anomalydetection.backend.engine.ema_engine import EMADetector


class TestEMADetector(unittest.TestCase):

    WINDOW = 20

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        observations = []
        posible_values = [4, 5, 6, 7, 8]
        for w in range(0, 6):
            for h in range(0, 23):
                for m in range(0, 59):
                    if m % 15 == 0:
                        v = random.choice(posible_values)
                        observations.append([v, w, h, m])
        self.observations = np.array(observations)

    def test__ema(self):
        self.engine = EMADetector(window=self.WINDOW)
        ema = self.engine._ema(self.observations, len(self.observations))
        self.assertAlmostEqual(ema[0], 6.0, places=0)

    def test__std(self):
        self.engine = EMADetector(window=self.WINDOW)
        std = self.engine._calc_std(self.observations)
        self.assertAlmostEqual(std, 1.0, places=0)

    def test_predict(self):
        self.engine = EMADetector(window=self.WINDOW)
        posible_values = [4, 5, 6, 7, 8]
        for w in range(0, 6):
            for h in range(0, 23):
                for m in range(0, 59):
                    if m % 15 == 0:
                        v = random.choice(posible_values)
                        extra_data = {
                            "ts": datetime(2018, 1, 1) + timedelta(hours=h,
                                                                   minutes=m)
                        }
                        self.engine.predict(v, **extra_data)

        normal = self.engine.predict(6, **{"ts": datetime.now()})
        self.assertEqual(normal.is_anomaly, False)

        anomaly = self.engine.predict(12, **{"ts": datetime.now()})
        self.assertEqual(anomaly.is_anomaly, True)
