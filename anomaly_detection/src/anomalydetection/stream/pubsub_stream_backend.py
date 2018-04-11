# -*- coding:utf-8 -*-

import base64
import logging
from collections import Generator

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from anomalydetection.stream import StreamBackend


class PubSubStreamBackend(StreamBackend):

    logger = logging.getLogger('PubSubStreamBackend')

    def __init__(self,
                 project_id: str,
                 auth_file: str,
                 input_topic: str,
                 subscriber: str) -> None:
        """
        PubSub Stream backend constructor.

        :type project_id:   str.
        :param project_id:  the Google Cloud Platform ProjectId.
        :type auth_file:    str.
        :param auth_file:   authentication json file.
        :type input_topic:        str.
        :param input_topic:       the PubSub Topic.
        :type subscriber:   str.
        :param subscriber:  the PubSub Subscriber name.
        """
        super().__init__()
        self.project_id = project_id
        self.topic = input_topic
        self.credentials = Credentials.from_service_account_file(auth_file)
        self.subscriber = subscriber
        self.pubsub = build('pubsub', 'v1', credentials=self.credentials)

    def __full_topic_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "topics",
                                          self.topic)

    def __full_subscription_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "subscriptions",
                                          self.subscriber)

    def poll(self) -> Generator:
        subscription = self.__full_subscription_name()
        body = {"returnImmediately": False, "maxMessages": 100}
        resp = self.pubsub.projects()\
            .subscriptions()\
            .pull(subscription=subscription, body=body)\
            .execute(num_retries=3)

        messages = resp.get("receivedMessages")
        if messages:
            ack_ids = []
            for i in messages:
                message = i.get("message")
                if message:
                    yield base64.b64decode(message["data"])
                    ack_ids.append(i.get("ackId"))
            ack_body = {"ackIds": ack_ids}

            self.pubsub.projects()\
                .subscriptions()\
                .acknowledge(subscription=subscription, body=ack_body)\
                .execute(num_retries=3)

    def push(self, message: str) -> None:
        encoded = base64.b64encode(message.encode("utf-8"))
        body = {"messages": [{"data": str(encoded, "utf-8")}]}
        resp = self.pubsub.projects()\
            .topics()\
            .publish(topic=self.__full_topic_name(),
                     body=body) \
            .execute(num_retries=3)

        self.logger.info(resp)

