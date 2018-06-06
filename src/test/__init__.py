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
    "SQLITE_DATABASE_FILE": os.getenv("SQLITE_DATABASE_FILE", "/tmp/database.sqlite"),
}

os.environ["SQLITE_DATABASE_FILE"] = config["SQLITE_DATABASE_FILE"]
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
os.environ["PUBSUB_PROJECT_ID"] = "testing"
os.environ["ASYNC_TEST_TIMEOUT"] = "100"
