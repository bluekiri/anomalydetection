# -*- coding:utf-8 -*- #

import logging

from anomalydetection.backend.conf.config import PERIOD_IN_MILLISECONDS, \
    SQLITE_DATABASE_FILE
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor
from anomalydetection.backend.repository.sqlite import SQLiteRepository, ObservableSQLite
from anomalydetection.backend.store_middleware.sqlite_store_middleware import \
    SQLiteStoreMiddleware
from anomalydetection.backend.stream.stream_factory import StreamFactory

logging.basicConfig()
logger = logging.getLogger()


def main():
    logger.info("Anomaly detection starting")

    # Creates stream based on config env vars and a RobustDetector
    stream = StreamFactory.create_stream()
    engine = RobustDetector(30)

    # Creates a store_middleware that stores all output to a file
    repository = SQLiteRepository(SQLITE_DATABASE_FILE)
    middleware = SQLiteStoreMiddleware(repository)
    warm_up = ObservableSQLite(repository)

    interactor = StreamEngineInteractor(
        stream,
        engine,
        InputJsonMessageHandler(),
        middleware=[middleware],
        warm_up=warm_up,
        agg_window_millis=PERIOD_IN_MILLISECONDS)
    interactor.run()


if __name__ == "__main__":
    main()
