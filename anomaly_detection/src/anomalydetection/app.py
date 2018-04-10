# -*- coding:utf-8 -*- #

import time
import logging

from rx.subjects import Subject

from anomalydetection.conf.config import *
from anomalydetection.interactor.engine.robust_z_engine import RobustDetector
from anomalydetection.interactor.anomaly_detection_kafka_bridge import AnomalyDetectionKafkaBridge
from anomalydetection.repository.kafka_repository import KafkaRepository

logger = logging.getLogger()


def main():
    # TODO workarround until fix the docker kafka service ready listener...
    time.sleep(15)
    logger.info("Anomaly detection Start")
    kafka_repository = KafkaRepository(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER.split(","), broker_list=KAFKA_BROKER_SERVER.split(","))
    anomaly_detector_engine = RobustDetector(window=30)

    subject = Subject()
    AnomalyDetectionKafkaBridge(source_observable=subject, anomaly_detection_engine=anomaly_detector_engine,
                                time_in_seconds=int(PERIOD_IN_SECONDS), kafka_repository=kafka_repository)
    for input_message in kafka_repository.listen_topic(topic=KAFKA_INPUT_TOPIC):
        subject.on_next(input_message)


if __name__ == "__main__":
    main()
