# -*- coding:utf-8 -*- #
import os
import time
import unittest
import threading

from anomalydetection.backend.stream.kafka_stream_backend import \
    KafkaStreamBackend
from rx import Observable
from test import LoggingMixin


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    def test(self):

        message = "hello world!"

        self.logger.info("Testing Kafka StreamBackend")
        kafka_broker = os.environ["KAFKA_BROKER"]
        kafka = KafkaStreamBackend(kafka_broker,
                                   kafka_broker,
                                   "test1",
                                   "test1",
                                   "test1")

        self.logger.info("Polling message")
        messages = kafka.poll()

        # Publish
        self.logger.info("Publishing message")

        def push_and_sleep(arg0):
            kafka.push(message)
            time.sleep(1)

        def raise_error():
            raise Exception("No message received")

        Observable.interval(10) \
            .map(push_and_sleep) \
            .subscribe(on_completed=raise_error)

        # Poll
        if messages:
            self.logger.info("Messages found, iterate it")
            for i in messages:
                self.logger.info("Next: {}".format(i))
                self.assertEqual(message, i)
                kafka.kafka_consumer.unsubscribe()
                break
        else:
            raise Exception("Cannot consume published message.")

