# -*- coding:utf-8 -*-

import os
import logging
from collections import Generator
from queue import Queue

from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud import pubsub

from anomalydetection.backend.stream import BaseStreamBackend


class PubSubStreamBackend(BaseStreamBackend):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self,
                 project_id: str,
                 subscription: str,
                 output_topic: str,
                 auth_file: str = None) -> None:

        super().__init__()
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.topic = output_topic
        self.subscription = subscription
        self.queue = Queue()
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        self.subs = self.subscriber.subscribe(self._full_subscription_name(),
                                              callback=self.__enqueue)

    def _full_topic_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "topics",
                                          self.topic)

    def _full_subscription_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "subscriptions",
                                          self.subscription)

    def __enqueue(self, message: Message) -> None:
        self.logger.debug(
            "Message received: {}".format(str(message.data, "utf-8")))
        self.queue.put(message)

    def __dequeue(self) -> Message:
        return self.queue.get()

    def poll(self) -> Generator:
        while True:
            message = self.__dequeue()
            message.ack()
            yield str(message.data, "utf-8")

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            encoded = message.encode("utf-8")
            self.publisher.publish(self._full_topic_name(), encoded)
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)
