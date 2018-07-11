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

from anomalydetection.backend.core.config import Config
from anomalydetection.backend.engine.builder import CADDetectorBuilder
from anomalydetection.backend.engine.builder import EMADetectorBuilder
from anomalydetection.backend.engine.builder import RobustDetectorBuilder
from anomalydetection.backend.repository.builder import SQLiteBuilder
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from anomalydetection.backend.sink.repository import RepositorySink
from anomalydetection.backend.sink.stream import StreamSink
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.builder import KafkaStreamConsumerBuilder
from anomalydetection.backend.stream.builder import PubSubStreamConsumerBuilder
from anomalydetection.backend.stream.kafka import KafkaStreamProducer
from anomalydetection.backend.stream.pubsub import PubSubStreamProducer
from anomalydetection.common.logging import LoggingMixin

from test import TEST_PATH


class TestConfig(unittest.TestCase, LoggingMixin):

    MODE = "test"
    DB_FILE = "test_config.sqlite"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Initialize config
        cls.config = Config(
            cls.MODE,
            open("{}/anomdec_home_test/anomdec.yml".format(TEST_PATH)))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        try:
            os.remove(cls.DB_FILE)
        except FileNotFoundError as _:
            pass

    def test_mode(self):
        self.assertEqual(self.MODE, self.config.mode)

    def test_get_names(self):
        self.assertEqual([x["name"] for x in self.config.config["streams"]],
                         self.config.get_names())

    def test_get_websocket_url(self):
        self.assertEqual(self.config.config["websocket"],
                         self.config.get_websocket_url())

    def test__get_stream_kafka(self):
        kafka_stream = self.config._get_stream(
            {
                "source": {
                    "type": "kafka",
                    "params": {
                        "broker_servers": "localhost:9092",
                        "input_topic": "in",
                        "group_id": "group_id"
                    },
                },
                "aggregation": {
                    "agg_function": "avg",
                    "agg_window_millis": 60000
                }
            }
        )
        self.assertIsInstance(kafka_stream, KafkaStreamConsumerBuilder)
        self.assertEqual(kafka_stream.agg_window_millis, 60000)
        self.assertEqual(kafka_stream.agg_function, AggregationFunction.AVG)
        self.assertEqual(kafka_stream.broker_servers, "localhost:9092")
        self.assertEqual(kafka_stream.input_topic, "in")
        self.assertEqual(kafka_stream.group_id, "group_id")

    def test__get_stream_pubsub(self):
        pubsub_stream = self.config._get_stream(
            {
                "source": {
                    "type": "pubsub",
                    "params": {
                        "project_id": "project-id",
                        "auth_file": "/dev/null",
                        "subscription": "in",
                    },
                }
            }
        )
        self.assertIsInstance(pubsub_stream, PubSubStreamConsumerBuilder)
        self.assertEqual(pubsub_stream.project_id, "project-id")
        self.assertEqual(pubsub_stream.subscription, "in")
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

    def test__get_engine_ema(self):
        ema = self.config._get_engine(
            {
                "type": "ema",
                "params": {
                    "window": 45,
                    "threshold": 2.5
                }
            }
        )
        self.assertIsInstance(ema, EMADetectorBuilder)
        self.assertEqual(ema.window, 45)
        self.assertEqual(ema.threshold, 2.5)

    def test__get_sink_sqlite(self):
        sqlite_sink = self.config._get_sink(
            {
                "name": "sqlite",
                "type": "repository",
                "repository": {
                    "type": "sqlite",
                    "params": {
                        "database": self.DB_FILE
                    }
                }
            }
        )
        self.assertIsInstance(sqlite_sink, RepositorySink)
        self.assertIsInstance(sqlite_sink.repository, SQLiteRepository)

    def test__get_sink_kafka(self):
        kafka_stream = self.config._get_sink(
            {
                "name": "kafka",
                "type": "stream",
                "stream": {
                    "type": "kafka",
                    "params": {
                        "broker_servers": "localhost:9092",
                        "output_topic": "out"
                    }
                }
            }
        )
        self.assertIsInstance(kafka_stream, StreamSink)
        self.assertIsInstance(kafka_stream.producer, KafkaStreamProducer)

    def test__get_sink_pubsub(self):
        pubsub_stream = self.config._get_sink(
            {
                "name": "pubsub",
                "type": "stream",
                "stream": {
                    "type": "pubsub",
                    "params": {
                        "project_id": "project",
                        "output_topic": "out"
                    }
                }
            }
        )
        self.assertIsInstance(pubsub_stream, StreamSink)
        self.assertIsInstance(pubsub_stream.producer, PubSubStreamProducer)
