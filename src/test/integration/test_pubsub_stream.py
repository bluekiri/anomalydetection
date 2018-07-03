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

from unittest.mock import patch

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

    project = None

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
            except AlreadyExists:
                pass

            try:
                subscriber = SubscriberClient()
                subscriber.create_subscription(
                    subscriber.subscription_path(cls.project, subscription),
                    subscriber.topic_path(cls.project, subscription))
            except AlreadyExists:
                pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        publisher = PublisherClient()
        subscriber = SubscriberClient()

        for topic in ["test0", "test1"]:
            try:
                publisher.delete_topic(
                    publisher.topic_path(cls.project, topic))
            except Exception as ex:
                raise ex

            try:
                subscriber.delete_subscription(
                    subscriber.subscription_path(cls.project, topic))
            except Exception as ex:
                raise ex

    def test_pubsub_stream_backend(self):

        is_passed = False

        subscription = "test0"
        topic = "test0"

        pubsub_consumer = PubSubStreamConsumer(self.project, subscription,
                                               self.credentials)
        pubsub_producer = PubSubStreamProducer(self.project, topic,
                                               self.credentials)
        messages = pubsub_consumer.poll()

        def push(_):
            pubsub_producer.push(self.MESSAGE)

        def completed():
            pubsub_consumer.unsubscribe()
            self.assertEqual(is_passed, True)

        Observable.interval(1000) \
            .take(20) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        if messages:
            for msg in messages:
                self.assertEqual(self.MESSAGE, msg)
                pubsub_consumer.unsubscribe()
                is_passed = True
                break

            self.assertEqual(is_passed, True)
        else:
            raise Exception("Cannot consume published message.")

    @patch("anomalydetection.backend.stream.pubsub.SparkPubsubStreamConsumer.unsubscribe")
    @patch("anomalydetection.common.concurrency.Concurrency.run_process")
    def test_pubsub_stream_backend_spark(self, run_process, unsubscribe):

        is_passed = False

        unsubscribe.return_value = None
        run_process.side_effect = Concurrency.run_thread

        subscription = "test1"
        topic = "test1"

        pubsub_producer = PubSubStreamProducer(
            self.project,
            topic,
            self.credentials)

        agg_consumer = SparkPubsubStreamConsumer(
            self.project,
            subscription,
            AggregationFunction.AVG,
            10 * 1000,
            self.credentials,
            spark_opts={"timeout": 30},
            multiprocessing=True)

        def push(_):
            pubsub_producer.push(InputMessage("app", 1.5, datetime.now()).to_json())

        def completed():
            agg_consumer.unsubscribe()

        Observable.interval(1000) \
            .take(30) \
            .map(push) \
            .subscribe(on_completed=completed)

        messages = agg_consumer.poll()
        if messages:
            for message in messages:
                self.logger.info(message)
                is_passed = True
                break

        else:
            raise Exception("Cannot consume published message.")

        Concurrency.get_thread(agg_consumer.pid).join(30.0)
        self.assertEqual(is_passed, True)
