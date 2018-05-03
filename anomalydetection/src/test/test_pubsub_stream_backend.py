# -*- coding:utf-8 -*- #

import os
import time
import unittest

from google.cloud import pubsub

from anomalydetection.backend.stream.pubsub_stream_backend import \
    PubSubStreamBackend
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from rx import Observable


class TestPubSubStreamBackend(unittest.TestCase):

    def test(self):

        message = "hello world!"

        publisher = PublisherClient()
        publisher.create_topic(publisher.topic_path("testing", "test0"))
        publisher.create_topic(publisher.topic_path("testing", "test1"))

        subscriber = SubscriberClient()
        subscriber.create_subscription(
            subscriber.subscription_path("testing", "test0"),
            subscriber.topic_path("testing", "test0"))

        pubsub = PubSubStreamBackend(
            "testing",
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            "test0", "test1")

        def push_and_sleep(arg0):
            pubsub.push(message)
            time.sleep(1)

        def raise_error():
            raise Exception("No message received")

        Observable.interval(10) \
            .map(push_and_sleep) \
            .subscribe(on_completed=raise_error)

        # Poll
        messages = pubsub.poll()
        if messages:
            for msg in messages:
                self.assertEqual(message, msg)
        else:
            raise Exception("Cannot consume published message.")

