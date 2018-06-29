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

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1 import SubscriberClient
from rx import Observable

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.pubsub import PubSubStreamConsumer, \
    SparkPubsubStreamConsumer
from anomalydetection.backend.stream.pubsub import PubSubStreamProducer
from anomalydetection.common.logging import LoggingMixin


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    MESSAGE = """{"test": "test"}"""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.passed = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = os.environ.get("PUBSUB_PROJECT", "testing")
        cls.subscription = os.environ.get("PUBSUB_SUBSCRIPTION", "test0")
        cls.credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
        cls.topic = cls.subscription

        try:
            publisher = PublisherClient()
            publisher.create_topic(publisher.topic_path(cls.project,
                                                        cls.subscription))

            subscriber = SubscriberClient()
            subscriber.create_subscription(
                subscriber.subscription_path(cls.project, cls.subscription),
                subscriber.topic_path(cls.project, cls.subscription))
        except AlreadyExists:
            pass

    def test_pubsub_stream_backend(self):

        pubsub_consumer = PubSubStreamConsumer(self.project, self.subscription)
        pubsub_producer = PubSubStreamProducer(self.project, self.topic)
        messages = pubsub_consumer.poll()

        def push(arg0):
            if not self.passed and arg0 > 10:
                raise Exception("No message received")
            pubsub_producer.push(self.MESSAGE)

        def completed():
            self.assertEqual(self.passed, True)
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        if messages:
            for msg in messages:
                self.assertEqual(self.MESSAGE, msg)
                self.passed = True
                break
        else:
            raise Exception("Cannot consume published message.")

    @unittest.skip("This could not be tested with PubSub emulator.")
    def test_pubsub_stream_backend_spark(self):

        project = os.environ.get("PUBSUB_PROJECT", self.project)
        subscription = os.environ.get("PUBSUB_SUBSCRIPTION", self.subscription)
        credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
        pubsub_producer = PubSubStreamProducer(
            project,
            subscription,
            credentials)

        def push(arg0):
            if arg0 > 40 and not self.passed:
                raise Exception("No message received")
            pubsub_producer.push(
                InputMessage("app", 1.5, datetime.now()).to_json())

        def completed():
            self.assertEqual(self.passed, True)
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=completed)

        agg_consumer = SparkPubsubStreamConsumer(
            project,
            subscription,
            AggregationFunction.AVG,
            10 * 1000,
            credentials,
            spark_opts={"timeout": 30 * 1000})

        for message in agg_consumer.poll():
            self.logger.info(message)
            self.passed = True
