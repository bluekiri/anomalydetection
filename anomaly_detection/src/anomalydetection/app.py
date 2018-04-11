# -*- coding:utf-8 -*- #

import logging

from anomalydetection.conf.config import *
from anomalydetection.entities.json_input_message_handler import InputJsonMessageHandler
from anomalydetection.engine.robust_z_engine import RobustDetector
from anomalydetection.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.stream.stream_factory import StreamFactory

logger = logging.getLogger()


def main():

    logger.info("Anomaly detection starting")
    stream = StreamFactory.create_stream()  # Creates stream based on config env vars
    engine = RobustDetector(30)
    interactor = StreamEngineInteractor(stream,
                                        engine,
                                        InputJsonMessageHandler(),
                                        agg_window=PERIOD_IN_MILLISECONDS,
                                        agg_function=sum)
    interactor.run()


if __name__ == "__main__":
    main()
