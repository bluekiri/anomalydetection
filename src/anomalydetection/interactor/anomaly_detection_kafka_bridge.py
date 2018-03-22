from rx import Observable, Observer
from rx.subjects import Subject

from anomalydetection.conf.config import output_topic
from anomalydetection.entities.output_message import OutputMessage
from anomalydetection.repository.kafka_repository import KafkaRepository
from src.anomalydetection.interactor.anomaly_detection_engine.base_engine import BaseEngine


class AnomalyDetectionKafkaBridge:
    def __init__(self, source_observable: Observable, anomaly_detection_engine: BaseEngine, time_in_seconds: int,
                 kafka_repository: KafkaRepository):
        self.kafka_repository = kafka_repository
        self.time_in_seconds = time_in_seconds
        self.anomaly_detection_engine = anomaly_detection_engine

        observable_to_predict = self.mean_by_windows(source_observable)

        subject = self.map_output_result(observable=observable_to_predict)
        subject.subscribe(
            on_next=lambda item: self.kafka_repository.send_output_message(topic=output_topic, message_output=item))

    def map_output_result(self, observable: Observable) -> Subject:
        return observable.map(lambda item: {"application": item["application"],
                                            "results_anomaly": self.anomaly_detection_engine.predict(item["value"]),
                                            "value": item["value"]})

    def mean_by_windows(self, observable: Observable) -> Observable:
        def map_element(items):
            application = items[0].application
            # mean = sum(item.value for item in items) / len(items) if len(items) != 0 else 0
            sumation = sum(item.value for item in items)
            return {"application": application, "value": sumation}

        return observable.buffer_with_time(timespan=self.time_in_seconds * 1000).filter(
            lambda items: len(items) > 0).map(map_element)
