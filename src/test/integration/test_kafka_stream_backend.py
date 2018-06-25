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

from anomalydetection.backend.stream.kafka_stream_backend import \
    KafkaStreamBackend
from rx import Observable
from test import config


class TestKafkaStreamBackend(unittest.TestCase, LoggingMixin):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.passed = False
        self.kafka_broker = config["KAFKA_BROKER"]

    def test_kafka_stream_backend(self):

        message = "hello world!"

        self.logger.info("Testing Kafka StreamBackend")
        kafka = KafkaStreamBackend(self.kafka_broker,
                                   "test1",
                                   "test1",
                                   "test1")

        self.logger.info("Polling message")
        messages = kafka.poll()

        # Publish
        self.logger.info("Publishing message")

        def push(arg0):
            if not self.passed and arg0 > 10:
                raise Exception("No message received")
            kafka.push(message)

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
                self.assertEqual(message, i)
                self.passed = True
                kafka.poll_stream.kafka_consumer.unsubscribe()
                break
        else:
            raise Exception("Cannot consume published message.")
