# -*- coding:utf-8 -*- #

import unittest

from anomalydetection.backend.stream.kafka_stream_backend import \
    KafkaStreamBackend
from rx import Observable
from test import config
from test import LoggingMixin


class TestKafkaStreamBackend(unittest.TestCase, LoggingMixin):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.passed = False

    def test_kafka_stream_backend(self):

        message = "hello world!"

        self.logger.info("Testing Kafka StreamBackend")
        kafka_broker = config["KAFKA_BROKER"]
        kafka = KafkaStreamBackend(kafka_broker,
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

        def raise_error():
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=raise_error)

        # Poll
        if messages:
            self.logger.info("Messages found, iterate it")
            for i in messages:
                self.logger.info("Next: {}".format(i))
                self.assertEqual(message, i)
                self.passed = True
                kafka.kafka_consumer.unsubscribe()
                break
        else:
            raise Exception("Cannot consume published message.")
