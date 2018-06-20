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

from anomalydetection.backend.engine.builder import CADDetectorBuilder, \
    RobustDetectorBuilder
from anomalydetection.backend.repository.builder import SQLiteBuilder
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.builder import KafkaStreamBuilder, \
    PubSubStreamBuilder
from anomalydetection.common.config import Config
from anomalydetection.common.logging import LoggingMixin

from test import TEST_PATH


class TestConfig(unittest.TestCase, LoggingMixin):

    mode = "test"

    def setUp(self):
        super().setUp()

        # Initialize config
        self.config = Config(
            "test",
            open("{}/anomdec-test.yml".format(TEST_PATH)))

    def test_mode(self):
        self.assertEqual(self.mode, self.config.mode)

    def test_get_names(self):
        self.assertEqual([x["name"] for x in self.config.config["streams"]],
                         self.config.get_names())

    def test_get_websocket_url(self):
        self.assertEqual(self.config.config["websocket"],
                         self.config.get_websocket_url())

    def test__get_stream_kafka(self):
        kafka_stream = self.config._get_stream(
            {
                "backend": {
                    "type": "kafka",
                    "params": {
                        "brokers": "localhost:9092",
                        "in": "in",
                        "out": "out",
                        "group_id": "group_id"
                    },
                },
                "aggregation": {
                    "function": "avg",
                    "window_millis": 60000
                }
            }
        )
        self.assertIsInstance(kafka_stream, KafkaStreamBuilder)
        self.assertEqual(kafka_stream.agg_window_millis, 60000)
        self.assertEqual(kafka_stream.agg_function, AggregationFunction.AVG)
        self.assertEqual(kafka_stream.broker_server, "localhost:9092")
        self.assertEqual(kafka_stream.input_topic, "in")
        self.assertEqual(kafka_stream.output_topic, "out")
        self.assertEqual(kafka_stream.group_id, "group_id")

    def test__get_stream_pubsub(self):
        pubsub_stream = self.config._get_stream(
            {
                "backend": {
                    "type": "pubsub",
                    "params": {
                        "project": "project-id",
                        "auth_file": "/dev/null",
                        "in": "in",
                        "out": "out",
                    },
                }
            }
        )
        self.assertIsInstance(pubsub_stream, PubSubStreamBuilder)
        self.assertEqual(pubsub_stream.project_id, "project-id")
        self.assertEqual(pubsub_stream.subscription, "in")
        self.assertEqual(pubsub_stream.output_topic, "out")
        self.assertEqual(pubsub_stream.auth_file, "/dev/null")

    def test__get_repository_sqlite(self):
        repository = self.config._get_repository(
            {
                "type": "sqlite",
                "params": {
                    "database": "/dev/null"
                }
            }
        )
        self.assertIsInstance(repository, SQLiteBuilder)
        self.assertEqual(repository.database, "/dev/null")

    def test__get_engine_cad(self):
        cad = self.config._get_engine(
            {
                "type": "cad",
                "params": {
                    "min_value": 1,
                    "max_value": 2,
                    "rest_period": 3,
                    "num_norm_value_bits": 4,
                    "max_active_neurons_num": 5,
                    "max_left_semi_contexts_length": 6
                }
            }
        )
        self.assertIsInstance(cad, CADDetectorBuilder)
        self.assertEqual(cad.min_value, 1)
        self.assertEqual(cad.max_value, 2)
        self.assertEqual(cad.rest_period, 3)
        self.assertEqual(cad.num_norm_value_bits, 4)
        self.assertEqual(cad.max_active_neurons_num, 5)
        self.assertEqual(cad.max_left_semi_contexts_length, 6)

    def test__get_engine_robust(self):
        robust = self.config._get_engine(
            {
                "type": "robust",
                "params": {
                    "window": 10,
                    "threshold": 0.999
                }
            }
        )
        self.assertIsInstance(robust, RobustDetectorBuilder)
        self.assertEqual(robust.window, 10)
        self.assertEqual(robust.threshold, 0.999)
