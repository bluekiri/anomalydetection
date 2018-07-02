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

from mock import patch
from rx import Observable

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream.agg.functions import AggregationFunction
from anomalydetection.backend.stream.kafka import KafkaStreamConsumer
from anomalydetection.backend.stream.kafka import SparkKafkaStreamConsumer
from anomalydetection.backend.stream.kafka import KafkaStreamProducer
from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.logging import LoggingMixin


class TestKafkaStreamBackend(unittest.TestCase, LoggingMixin):

    MESSAGE = """{"test": "test"}"""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.kafka_broker = os.environ.get("KAFKA_BROKER", "localhost:9092")

    def test_kafka_stream_backend(self):

        is_passed = False

        self.logger.info("Testing Kafka StreamBackend")
        kafka_consumer = KafkaStreamConsumer(self.kafka_broker, "test1", "test1")
        kafka_producer = KafkaStreamProducer(self.kafka_broker, "test1")

        def push(_):
            kafka_producer.push(self.MESSAGE)

        def completed():
            kafka_consumer.unsubscribe()
            self.assertEqual(is_passed, True)

        Observable.interval(1000) \
            .take(20) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        messages = kafka_consumer.poll()
        if messages:
            for message in messages:
                self.assertEqual(message, self.MESSAGE)
                kafka_consumer.unsubscribe()
                is_passed = True
                break
            self.assertEqual(is_passed, True)
        else:
            raise Exception("Cannot consume published message.")

    @patch("anomalydetection.common.concurrency.Concurrency.run_process")
    def test_kafka_stream_backend_spark(self, run_process):

        run_process.side_effect = Concurrency.run_thread

        is_passed = False

        topic = "test2"
        group_id = "test2"
        kafka_producer = KafkaStreamProducer(self.kafka_broker, "test2")

        agg_consumer = SparkKafkaStreamConsumer(
            self.kafka_broker,
            topic,
            group_id,
            AggregationFunction.AVG,
            10 * 1000,
            spark_opts={"timeout": 20 * 1000})

        def push(_):
            kafka_producer.push(InputMessage("app", 1.5, datetime.now()).to_json())

        def completed():
            agg_consumer.unsubscribe()
            self.assertEqual(is_passed, True)
            Concurrency.kill_process(agg_consumer.pid)

        Observable.interval(1000) \
            .take(40) \
            .map(push) \
            .subscribe(on_completed=completed)

        messages = agg_consumer.poll()
        if messages:
            for message in messages:
                self.logger.info(message)
                is_passed = True
                agg_consumer.unsubscribe()
                break

            self.assertEqual(is_passed, True)
        else:
            raise Exception("Cannot consume published message.")
