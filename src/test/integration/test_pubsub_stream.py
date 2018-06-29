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

from anomalydetection.common.concurrency import Concurrency
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1 import SubscriberClient
from rx import Observable

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.pubsub import PubSubStreamConsumer
from anomalydetection.backend.stream.pubsub import SparkPubsubStreamConsumer
from anomalydetection.backend.stream.pubsub import PubSubStreamProducer
from anomalydetection.common.logging import LoggingMixin


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    MESSAGE = """{"test": "test"}"""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def setUp(self):
        super().setUp()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = os.environ.get("PUBSUB_PROJECT", "testing")
        cls.credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)

        for subscription in ["test0", "test1"]:
            try:
                publisher = PublisherClient()
                publisher.create_topic(publisher.topic_path(cls.project,
                                                            subscription))

                subscriber = SubscriberClient()
                subscriber.create_subscription(
                    subscriber.subscription_path(cls.project, subscription),
                    subscriber.topic_path(cls.project, subscription))
            except AlreadyExists:
                pass

    def test_pubsub_stream_backend(self):

        pubsub_consumer = PubSubStreamConsumer(self.project, "test0")
        pubsub_producer = PubSubStreamProducer(self.project, "test0")
        messages = pubsub_consumer.poll()

        def push(_):
            pubsub_producer.push(self.MESSAGE)

        def completed():
            self.assertEqual(self.passed, True)

        Observable.interval(1000) \
            .take(20) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        if messages:
            for msg in messages:
                self.assertEqual(self.MESSAGE, msg)
                self.passed = True
                break

            self.assertEqual(self.passed, True)
        else:
            raise Exception("Cannot consume published message.")

    @unittest.skip("FIXME: This could not be tested with PubSub emulator.")
    def test_pubsub_stream_backend_spark(self):

        project = os.environ.get("PUBSUB_PROJECT", self.project)
        subscription = os.environ.get("PUBSUB_SUBSCRIPTION", "test1")
        credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)

        pubsub_producer = PubSubStreamProducer(
            project,
            subscription,
            credentials)

        agg_consumer = SparkPubsubStreamConsumer(
            project,
            subscription,
            AggregationFunction.AVG,
            10 * 1000,
            credentials,
            spark_opts={"timeout": 20 * 1000})

        def push(_):
            pubsub_producer.push(InputMessage("app", 1.5, datetime.now()).to_json())

        def completed():
            agg_consumer.unsubscribe()
            self.assertEqual(self.passed, True)
            self.completed = True
            Concurrency.kill_process(agg_consumer.pid)

        Observable.interval(1000) \
            .take(40) \
            .map(push) \
            .subscribe(on_completed=completed)

        messages = agg_consumer.poll()
        if messages:
            for message in messages:
                self.logger.info(message)
                self.assertEqual(message, self.MESSAGE)
                self.passed = True
                agg_consumer.unsubscribe()
                break

            self.assertEqual(self.passed, True)
        else:
            raise Exception("Cannot consume published message.")
