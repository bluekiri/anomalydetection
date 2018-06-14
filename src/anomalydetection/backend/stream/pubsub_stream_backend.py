# -*- coding:utf-8 -*-
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
from collections import Generator
from queue import Queue

from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud import pubsub

from anomalydetection.backend.stream import BaseStreamBackend, \
    BasePollingStream, BasePushingStream
from anomalydetection.common.logging import LoggingMixin


class PubSubPollingStream(BasePollingStream, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 subscription: str,
                 auth_file: str = None) -> None:

        super().__init__()
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.subscription = subscription
        self.queue = Queue()
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        self.subs = self.subscriber.subscribe(self._full_subscription_name(),
                                              callback=self.__enqueue)

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

    def __str__(self) -> str:
        return "PubSub subscription: {}".format(self._full_subscription_name())


class PubSubPushingStream(BasePushingStream, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 topic: str,
                 auth_file: str = None) -> None:

        super().__init__()
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.topic = topic
        self.queue = Queue()
        self.publisher = pubsub.PublisherClient()

    def _full_topic_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "topics",
                                          self.topic)

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            encoded = message.encode("utf-8")
            self.publisher.publish(self._full_topic_name(), encoded)
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)

    def __str__(self) -> str:
        return "PubSub topic: {}".format(self._full_topic_name())


class PubSubStreamBackend(BaseStreamBackend, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 subscription: str,
                 output_topic: str,
                 auth_file: str = None) -> None:

        super().__init__(
            PubSubPollingStream(project_id, subscription, auth_file),
            PubSubPushingStream(project_id, output_topic, auth_file))
