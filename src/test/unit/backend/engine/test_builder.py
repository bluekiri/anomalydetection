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

from anomalydetection.backend.engine.builder import *


class TestBaseBuilder(unittest.TestCase):

    def test_build(self):
        with self.assertRaises(NotImplementedError) as ctx:
            builder = BaseBuilder()
            builder.build()

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")


class TestCADDetectorBuilder(unittest.TestCase):

    MIN_VALUE = 20
    MAX_VALUE = 400
    THRESHOLD = .99
    REST_PERIOD = 35
    MAX_LEFT = 1000
    MAX_NEURONS = 10
    NORM_BITS = 5

    def setUp(self):
        super().setUp()
        self.builder = CADDetectorBuilder()

    def test_set_min_value(self):
        self.builder.set_min_value(self.MIN_VALUE)
        self.assertEqual(self.builder.min_value, self.MIN_VALUE)

    def test_set_max_value(self):
        self.builder.set_max_value(self.MAX_VALUE)
        self.assertEqual(self.builder.max_value, self.MAX_VALUE)

    def test_set_threshold(self):
        self.builder.set_threshold(self.THRESHOLD)
        self.assertEqual(self.builder.threshold, self.THRESHOLD)

    def test_rest_period(self):
        self.builder.set_rest_period(self.REST_PERIOD)
        self.assertEqual(self.builder.rest_period, self.REST_PERIOD)

    def test_set_max_left_semi_contexts_length(self):
        self.builder.set_max_left_semi_contexts_length(self.MAX_LEFT)
        self.assertEqual(self.builder.max_left_semi_contexts_length,
                         self.MAX_LEFT)

    def test_set_max_active_neurons_num(self):
        self.builder.set_max_active_neurons_num(self.MAX_NEURONS)
        self.assertEqual(self.builder.max_active_neurons_num, self.MAX_NEURONS)

    def test_set_num_norm_value_bits(self):
        self.builder.set_num_norm_value_bits(self.NORM_BITS)
        self.assertEqual(self.builder.num_norm_value_bits, self.NORM_BITS)


class TestRobustDetectorBuilder(unittest.TestCase):

    WINDOW = 10
    THRESHOLD = .99

    def setUp(self):
        super().setUp()
        self.builder = RobustDetectorBuilder()

    def test_set_window(self):
        self.builder.set_window(self.WINDOW)
        self.assertEqual(self.builder.window, self.WINDOW)

    def test_set_threshold(self):
        self.builder.set_threshold(self.THRESHOLD)
        self.assertEqual(self.builder.threshold, self.THRESHOLD)


class TestEngineBuilderFactory(unittest.TestCase):

    def test_get_robust(self):
        builder = EngineBuilderFactory.get_robust()
        self.assertIsInstance(builder, RobustDetectorBuilder)

    def test_get_cad(self):
        builder = EngineBuilderFactory.get_cad()
        self.assertIsInstance(builder, CADDetectorBuilder)