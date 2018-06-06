# -*- coding:utf-8 -*- #

import unittest
import test
from google.api_core.exceptions import AlreadyExists

from anomalydetection.backend.stream.pubsub_stream_backend import \
    PubSubStreamBackend
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from rx import Observable


class TestPubSubStreamBackend(unittest.TestCase, test.LoggingMixin):

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

        pubsub = PubSubStreamBackend("testing",
                                     "test0",
                                     "test0")
        messages = pubsub.poll()

        def push(arg0):
            if not self.passed and arg0 > 10:
                raise Exception("No message received")
            pubsub.push(message)

        def completed():
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
