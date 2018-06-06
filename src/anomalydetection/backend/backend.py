# -*- coding:utf-8 -*- #

import json
import logging
import multiprocessing
import random
import threading

from rx import Observable

from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.config import Config
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor

logging.basicConfig()
logger = logging.getLogger(__name__)


def produce_messages(config: Config):

    vals = [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [12, 23, 40, 51, 100]  # <- Anomalies

    apps = ["devel0", "devel1", "devel2"]

    def push(i, publisher):
        logger.info("Sending message number {}".format(i))
        from datetime import datetime
        for app in apps:
            random.shuffle(vals)
            publisher.push(json.dumps({
                "application": app,
                "ts": str(datetime.now()),
                "value": vals[0]
            }))

    # Send a message each 10ms
    publishers = config.build_publishers()
    Observable.interval(10000).subscribe(lambda i: push(i, publishers[0]))
    # Observable.interval(10000).subscribe(lambda i: push(i, publishers[1]))


def main(config: Config):

    logger.info("Anomaly detection starting")

    # Creates stream based on config env vars and a RobustDetector
    def run_live_anomaly_detection(stream, engine_builder, middlewares, warmup):
        interactor = StreamEngineInteractor(
            stream,
            engine_builder,
            InputJsonMessageHandler(),
            middleware=middlewares,
            warm_up=warmup[0])
        interactor.run()

    for name, item in config.get_as_dict().items():
        Concurrency.run_thread(target=run_live_anomaly_detection,
                               args=item, name="Detector {}".format(name))


if __name__ == "__main__":
    main(Config())
