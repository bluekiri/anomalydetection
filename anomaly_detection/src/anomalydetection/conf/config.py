# -*- coding:utf-8 -*- #
import os


def get_or_default(key: str, default: object=None):
    """
    Get value by key or default value instead.
    :param key:       the key name.
    :param default:   default value.
    :return:          the value if is present, or default instead.
    """
    if key in os.environ:
        return os.environ[key]
    else:
        return default


# General
PERIOD_IN_SECONDS = get_or_default("PERIOD_IN_SECONDS", 300)

# Kafka
KAFKA_BOOTSTRAP_SERVER = get_or_default("KAFKA_BOOTSTRAP_SERVER")
KAFKA_BROKER_SERVER = get_or_default("KAFKA_BROKER_SERVER")
KAFKA_INPUT_TOPIC = get_or_default("KAFKA_INPUT_TOPIC")
KAFKA_OUTPUT_TOPIC = get_or_default("KAFKA_OUTPUT_TOPIC")

# Pub/Sub
PUBSUB_PROJECT_ID = get_or_default("PUBSUB_PROJECT_ID")
PUBSUB_INPUT_TOPIC = get_or_default("PUBSUB_OUTPUT_TOPIC")
PUBSUB_OUTPUT_TOPIC = get_or_default("PUBSUB_OUTPUT_TOPIC")
