# -*- coding:utf-8 -*- #

import logging

from anomalydetection.conf.config import *
from anomalydetection.entities.json_input_message_handler import InputJsonMessageHandler
from anomalydetection.engine.robust_z_engine import RobustDetector
from anomalydetection.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.stream import Middleware
from anomalydetection.stream.stream_factory import StreamFactory

logging.basicConfig()
logger = logging.getLogger()


class StoreToFileMiddleware(Middleware):

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename

    def on_next(self, value):
        file = open(self.filename, "a")
        file.write(str(value) + "\n")
        file.close()

    def on_error(self, error):
        logger.error(error)

    def on_completed(self):
        logger.info("Completed!")


def main():

    logger.info("Anomaly detection starting")

    # Creates stream based on config env vars and a RobustDetector
    stream = StreamFactory.create_stream()
    engine = RobustDetector(30)

    # Creates a middleware that stores all output to a file
    middleware = StoreToFileMiddleware("/tmp/backend_storage.json")

    interactor = StreamEngineInteractor(
        stream,
        engine,
        InputJsonMessageHandler(),
        middleware=[middleware],
        agg_window_millis=PERIOD_IN_MILLISECONDS,
        agg_function=sum)
    interactor.run()


if __name__ == "__main__":
    main()
