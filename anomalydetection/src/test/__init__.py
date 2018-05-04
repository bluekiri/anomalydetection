# -*- coding:utf-8 -*- #

import logging
import os

TEST_PATH = os.path.realpath(os.path.dirname(__file__))


class LoggingMixin(object):

    logging.basicConfig()
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)


config = {
    "KAFKA_BROKER": os.getenv("KAFKA_BROKER", "localhost:9092"),
    "DATA_DB_FILE": os.getenv("DATA_DB_FILE", "/tmp/database.sqlite"),
}

os.environ["DATA_DB_FILE"] = config["DATA_DB_FILE"]
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
os.environ["PUBSUB_PROJECT_ID"] = "testing"
