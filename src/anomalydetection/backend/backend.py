# -*- coding:utf-8 -*- #
import json
import logging
import random
import time

from rx import Observable, Observer

from anomalydetection.backend.middleware.queue_middleware import \
    WebSocketDashboardMiddleware
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

    class IntervalObserver(Observer):

        def __init__(self, publisher) -> None:
            super().__init__()
            self.publisher = publisher

        def push(self, value):
            logger.info("Sending message number {}".format(value))
            from datetime import datetime
            for app in apps:
                random.shuffle(vals)
                self.publisher.push(json.dumps({
                    "application": app,
                    "ts": str(datetime.now()),
                    "value": vals[0]
                }))

        def on_next(self, value):
            return self.push(value)

        def on_error(self, error):
            return super().on_error(error)

        def on_completed(self):
            return super().on_completed()

    # Send a message each 10ms
    time.sleep(10)
    publishers = config.build_publishers()
    for pub in publishers:
        Observable.interval(5000).subscribe(IntervalObserver(pub.push_stream))


def main(config: Config):

    logger.info("Anomaly detection starting")

    # Creates stream based on config env vars and a RobustDetector
    def run_live_anomaly_detection(stream, engine_builder,
                                   middlewares, warmup, name):

        # Send to broker or similar
        extra_middleware = [
            WebSocketDashboardMiddleware(name)
        ]

        # Instantiate interactor and run
        interactor = StreamEngineInteractor(
            stream,
            engine_builder,
            InputJsonMessageHandler(),
            middleware=middlewares + extra_middleware,
            warm_up=warmup[0])
        interactor.run()

    for name, item in config.get_as_dict().items():
        item_list = list(item)
        item_list.append(name)
        Concurrency.run_thread(target=run_live_anomaly_detection,
                               args=tuple(item_list),
                               name="Detector {}".format(name))


if __name__ == "__main__":
    main(Config())
