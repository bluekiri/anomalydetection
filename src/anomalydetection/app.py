import logging

from rx.subjects import Subject

from anomalydetection.conf.config import bootstrap_server, input_topic, broker_server
from anomalydetection.interactor.anomaly_detection_engine.dummy_engine import DummyEngine
from anomalydetection.interactor.anomaly_detection_kafka_bridge import AnomalyDetectionKafkaBridge
from anomalydetection.repository.kafka_repository import KafkaRepository
import time

logger = logging.getLogger()


def main():
    time.sleep(15)
    logger.info("Anomaly detection Start")
    kafka_repository = KafkaRepository(bootstrap_servers=bootstrap_server, broker_list=broker_server)
    dummy_engine = DummyEngine()

    subject = Subject()
    AnomalyDetectionKafkaBridge(source_observable=subject, anomaly_detection_engine=dummy_engine, time_in_seconds=5,
                                kafka_repository=kafka_repository)
    for input_message in kafka_repository.listen_topic(topic=input_topic):
        subject.on_next(input_message)


if __name__ == "__main__":
    main()
