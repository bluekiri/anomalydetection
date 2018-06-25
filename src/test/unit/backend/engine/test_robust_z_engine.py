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

import numpy as np
import unittest

from anomalydetection.backend.entities.output_message import AnomalyResult

from anomalydetection.backend.engine.robust_z_engine import RobustDetector


class TestRobustDetector(unittest.TestCase):

    WINDOW = 4

    def setUp(self):
        super().setUp()
        self.engine = None

    def test__update_buffer(self):

        self.engine = RobustDetector(window=self.WINDOW, threshold=0.999)

        test_values = map(float, [1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 1, 2])
        windows = [
            [np.nan, np.nan, np.nan, 1],
            [np.nan, np.nan, 1, 2],
            [np.nan, 1, 2, 1],
            [1, 2, 1, 2],
            [2, 1, 2, 1],
            [1, 2, 1, 2],
            [2, 1, 2, 1],
            [1, 2, 1, 2],
            [2, 1, 2, 3],
            [1, 2, 3, 1],
            [2, 3, 1, 2],
            [3, 1, 2, 3],
            [1, 2, 3, 1],
            [2, 3, 1, 2],
            [3, 1, 2, 1],
            [1, 2, 1, 2]
        ]

        for i, val in enumerate(test_values):
            self.engine._update_buffer(val)
            actual = self.engine._data.flatten()
            expected = np.array(windows[i])
            self.assertEqual(actual.all(), expected.all())

    def test__update_statistics(self):

        self.engine = RobustDetector(window=self.WINDOW, threshold=0.999)

        test_values = [1, 2, 1, 2]
        for i, val in enumerate(test_values):
            self.engine._update_buffer(val)

        self.engine._update_statistics()
        self.assertEqual(self.engine._median, 1.5)
        self.assertEqual(self.engine._mad, 0.741301109252801)

    def test__update(self):

        self.engine = RobustDetector(window=self.WINDOW, threshold=0.999)

        test_values = [1, 2, 1, 2, 5, 5, 5, 2]
        statistics = [
            [np.nan, np.nan],
            [np.nan, np.nan],
            [np.nan, np.nan],
            [1.5, 0.741301109252801],
            [2.0, 0.741301109252801],
            [3.5, 2.223903327758403],
            [5, 0.0],
            [5, 0.0],
        ]

        for i, val in enumerate(test_values):
            self.engine._update(val)
            actual = [self.engine._median, self.engine._mad]
            expected = statistics[i]
            # FIXME: Assert list equals
            self.assertListEqual(actual, expected)

    def test_predict(self):

        self.engine = RobustDetector(window=self.WINDOW, threshold=0.999)

        test_values = [1, 2, 1, 2, 5, 5, 5, 2]
        predictions = [
            AnomalyResult(-1, -1, -1, -1),
            AnomalyResult(-1, -1, -1, -1),
            AnomalyResult(-1, -1, -1, -1),
            AnomalyResult(-1, -1, -1, -1),
            AnomalyResult(-0.7907926364110414,
                          3.7907926364110414,
                          0.9999988290287686,
                          1),
            AnomalyResult(-0.29079263641104136,
                          4.290792636411041,
                          0.999974054066204,
                          1),
            AnomalyResult(-3.3723779092331236,
                          10.372377909233123,
                          0.75,
                          0),
            AnomalyResult(5.0, 5.0, 1.0, 1),
        ]

        for i, val in enumerate(test_values):
            actual = self.engine.predict(val).to_dict()
            expected = predictions[i].to_dict()
            self.assertDictEqual(actual, expected)
