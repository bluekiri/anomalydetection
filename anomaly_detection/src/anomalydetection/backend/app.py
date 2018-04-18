# -*- coding:utf-8 -*- #

import logging

from anomalydetection.backend.conf.config import PERIOD_IN_MILLISECONDS
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor
from anomalydetection.backend.store_middleware.sqlite_store_middleware import \
    SqliteStoreMiddleware
from anomalydetection.backend.stream.stream_factory import StreamFactory

logging.basicConfig()
logger = logging.getLogger()


def main():
    logger.info("Anomaly detection starting")

    # Creates stream based on config env vars and a RobustDetector
    stream = StreamFactory.create_stream()
    engine = RobustDetector(30)

    # Creates a store_middleware that stores all output to a file
    middleware = SqliteStoreMiddleware(logger)

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
