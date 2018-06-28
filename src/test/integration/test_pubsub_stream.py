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

from google.api_core.exceptions import AlreadyExists

from anomalydetection.backend.stream.pubsub import PubSubStreamConsumer
from anomalydetection.backend.stream.pubsub import PubSubStreamProducer
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from rx import Observable

from anomalydetection.common.logging import LoggingMixin


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.passed = False

    def test_pubsub_stream_backend(self):

        message = "hello world!"

        try:
            publisher = PublisherClient()
            publisher.create_topic(publisher.topic_path("testing", "test0"))

            subscriber = SubscriberClient()
            subscriber.create_subscription(
                subscriber.subscription_path("testing", "test0"),
                subscriber.topic_path("testing", "test0"))
        except AlreadyExists:
            pass

        pubsub_consumer = PubSubStreamConsumer("testing", "test0")
        pubsub_producer = PubSubStreamProducer("testing", "test0")
        messages = pubsub_consumer.poll()

        def push(arg0):
            if not self.passed and arg0 > 10:
                raise Exception("No message received")
            pubsub_producer.push(message)

        def completed():
            self.assertEqual(self.passed, True)
            self.logger.debug("Completed")

        Observable.interval(1000) \
            .map(push) \
            .subscribe(on_completed=completed)

        # Poll
        if messages:
            for msg in messages:
                self.assertEqual(message, msg)
                self.passed = True
                break
        else:
            raise Exception("Cannot consume published message.")
