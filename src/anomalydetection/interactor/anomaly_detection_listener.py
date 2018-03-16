from rx import Observable, Observer
from rx.subjects import Subject

from src.anomalydetection.interactor.anomaly_detection_engine.base_engine import BaseEngine


class AnomalyDetectionListener:
    def __init__(self, observable: Observable, anomaly_detection_engine: BaseEngine, time_in_seconds: int):
        self.time_in_seconds = time_in_seconds
        self.anomaly_detection_engine = anomaly_detection_engine
        self.observable = observable
        self.observer = AnomalyDetectionListener.AnomalyDetectionObserver(self.anomaly_detection_engine)
        observable_to_predict = self.mean_by_windows(self.observable)
        observable_to_predict.subscribe(self.observer)

    def mean_by_windows(self, observable: Observable) -> Observable:
        return observable.buffer_with_time(timespan=self.time_in_seconds * 1000).map(
            lambda items: sum(item.value for item in items) / len(items))

    class AnomalyDetectionObserver(Observer):
        def __init__(self, anomaly_detection_engine: BaseEngine):
            self.anomaly_detection_engine = anomaly_detection_engine
            super(AnomalyDetectionListener.AnomalyDetectionObserver, self).__init__()

        def on_next(self, value):
            self.anomaly_detection_engine.predict(value)
            pass

        def on_error(self, error):
            pass

        def on_completed(self):
            pass
