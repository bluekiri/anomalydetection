# -*- coding:utf-8 -*-
from anomalydetection.stream import StreamBackend
from anomalydetection.stream.kafka_stream_backend import KafkaStreamBackend
from anomalydetection.stream.pubsub_stream_backend import PubSubStreamBackend
from anomalydetection.conf.config import *


class StreamFactory(object):

    @staticmethod
    def create_stream() -> StreamBackend:
        if PUBSUB_PROJECT_ID and PUBSUB_INPUT_TOPIC and PUBSUB_OUTPUT_TOPIC:
            return StreamFactory.create_pubsub_stream()
        elif KAFKA_BOOTSTRAP_SERVER \
                and KAFKA_BROKER_SERVER \
                and KAFKA_INPUT_TOPIC \
                and KAFKA_OUTPUT_TOPIC:
            return StreamFactory.create_kafka_stream()

    @staticmethod
    def create_pubsub_stream() -> StreamBackend:
        return PubSubStreamBackend(
            PUBSUB_PROJECT_ID,
            PUBSUB_AUTH_FILE,
            PUBSUB_INPUT_TOPIC,
            PUBSUB_OUTPUT_TOPIC,
        )

    @staticmethod
    def create_kafka_stream() -> StreamBackend:
        return KafkaStreamBackend(
            KAFKA_BOOTSTRAP_SERVER,
            KAFKA_BROKER_SERVER,
            KAFKA_INPUT_TOPIC,
            KAFKA_OUTPUT_TOPIC,
            KAFKA_GROUP_ID)
