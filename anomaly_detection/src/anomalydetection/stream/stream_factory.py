# -*- coding:utf-8 -*-

from anomalydetection.stream import StreamBackend
from anomalydetection.stream.kafka_stream_backend import KafkaStreamBackend
from anomalydetection.stream.pubsub_stream_backend import PubSubStreamBackend
from anomalydetection.conf.config import *


class StreamFactory(object):

    @staticmethod
    def create_stream() -> StreamBackend:
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
    def create_pubsub_stream() -> StreamBackend:
        return PubSubStreamBackend(
            PUBSUB_PROJECT_ID,
            PUBSUB_SUBSCRIPTION,
            PUBSUB_OUTPUT_TOPIC,
            PUBSUB_AUTH_FILE)

    @staticmethod
    def create_kafka_stream() -> StreamBackend:
        return KafkaStreamBackend(
            KAFKA_BOOTSTRAP_SERVER,
            KAFKA_BROKER_SERVER,
            KAFKA_INPUT_TOPIC,
            KAFKA_OUTPUT_TOPIC,
            KAFKA_GROUP_ID)
