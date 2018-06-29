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

from anomalydetection.backend.stream.aggregation_functions import \
    AggregationFunction

from anomalydetection.backend.entities.input_message import InputMessage
from rx import Observable

from anomalydetection.backend.stream.kafka import KafkaStreamConsumer, \
    SparkKafkaStreamConsumer
from anomalydetection.backend.stream.kafka import KafkaStreamProducer
from anomalydetection.common.logging import LoggingMixin
from test import config


class TestKafkaStreamBackend(unittest.TestCase, LoggingMixin):

    MESSAGE = """{"test": "test"}"""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.passed = False
        self.kafka_broker = config["KAFKA_BROKER"]

    def test_kafka_stream_backend(self):

        self.logger.info("Testing Kafka StreamBackend")
        kafka_consumer = KafkaStreamConsumer(self.kafka_broker, "test1", "test1")
        kafka_producer = KafkaStreamProducer(self.kafka_broker, "test1")

        self.logger.info("Polling message")
        messages = kafka_consumer.poll()

        # Publish
        self.logger.info("Publishing message")

        def push(arg0):
            if not self.passed and arg0 > 10:
                raise Exception("No message received")
            kafka_producer.push(self.MESSAGE)

        def completed():
            self.assertEqual(self.passed, True)
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        if messages:
            self.logger.info("Messages found, iterate it")
            for i in messages:
                self.logger.info("Next: {}".format(i))
                self.assertEqual(self.MESSAGE, i)
                self.passed = True
                kafka_consumer._kafka_consumer.unsubscribe()
                break
        else:
            raise Exception("Cannot consume published message.")

    @unittest.skip("Spark timeout infinities this test.")
    def test_kafka_stream_backend_spark(self):

        topic = "test1"
        group_id = "test1"
        kafka_producer = KafkaStreamProducer(self.kafka_broker, "test1")

        def push(arg0):
            if arg0 > 40 and not self.passed:
                raise Exception("No message received")
            kafka_producer.push(
                InputMessage("app", 1.5, datetime.now()).to_json())

        def completed():
            self.assertEqual(self.passed, True)
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=completed)

        agg_consumer = SparkKafkaStreamConsumer(
            self.kafka_broker,
            topic,
            group_id,
            AggregationFunction.AVG,
            10 * 1000,
            spark_opts={"timeout": 30 * 1000})

        for message in agg_consumer.poll():
            self.logger.info(message)
            self.passed = True
