# -*- coding:utf-8 -*-
from anomalydetection.backend.conf.config import KAFKA_BOOTSTRAP_SERVER, \
    KAFKA_BROKER_SERVER, KAFKA_INPUT_TOPIC, KAFKA_OUTPUT_TOPIC, KAFKA_GROUP_ID, \
    PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION, PUBSUB_OUTPUT_TOPIC, \
    PUBSUB_AUTH_FILE
from anomalydetection.backend.stream import BaseStreamBackend
from anomalydetection.backend.stream.kafka_stream_backend import KafkaStreamBackend
from anomalydetection.backend.stream.pubsub_stream_backend import PubSubStreamBackend


class StreamFactory(object):

    @staticmethod
    def create_stream() -> BaseStreamBackend:
        if StreamFactory.is_pubsub():
            return StreamFactory.create_pubsub_stream()
        elif StreamFactory.is_kafka():
            return StreamFactory.create_kafka_stream()
        else:
            raise RuntimeError("Bad configuration, please set env vars for stream backend.")

    @staticmethod
    def is_kafka() -> bool:
        return KAFKA_BOOTSTRAP_SERVER \
               and KAFKA_BROKER_SERVER \
               and KAFKA_INPUT_TOPIC \
               and KAFKA_OUTPUT_TOPIC \
               and KAFKA_GROUP_ID

    @staticmethod
    def is_pubsub() -> bool:
        return PUBSUB_PROJECT_ID \
               and PUBSUB_SUBSCRIPTION \
               and PUBSUB_OUTPUT_TOPIC

    @staticmethod
    def create_pubsub_stream() -> BaseStreamBackend:
        return PubSubStreamBackend(
            PUBSUB_PROJECT_ID,
            PUBSUB_SUBSCRIPTION,
            PUBSUB_OUTPUT_TOPIC,
            PUBSUB_AUTH_FILE)

    @staticmethod
    def create_kafka_stream() -> BaseStreamBackend:
        return KafkaStreamBackend(
            KAFKA_BOOTSTRAP_SERVER,
            KAFKA_BROKER_SERVER,
            KAFKA_INPUT_TOPIC,
            KAFKA_OUTPUT_TOPIC,
            KAFKA_GROUP_ID)
