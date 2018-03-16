import logging

from rx.subjects import Subject

from anomalydetection.conf.config import bootstrap_server, input_topic
from anomalydetection.interactor.anomaly_detection_engine.dummy_engine import DummyEngine
from anomalydetection.interactor.anomaly_detection_listener import AnomalyDetectionListener
from anomalydetection.repository.kafka_repository import KafkaRepository

logger = logging.getLogger()


def main():
    logger.info("Anomaly detection Start")
    kafka_repository = KafkaRepository(bootstrap_servers=bootstrap_server)
    dummy_engine = DummyEngine()

    subject = Subject()
    AnomalyDetectionListener(observable=subject, anomaly_detection_engine=dummy_engine, time_in_seconds=10)
    for input_message in kafka_repository.listen_topic(topic=input_topic):
        subject.on_next(input_message)


if __name__ == "__main__":
    main()
