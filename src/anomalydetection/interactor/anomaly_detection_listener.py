from rx import Observable, Observer
from rx.subjects import Subject

from src.anomalydetection.interactor.anomaly_detection_engine.base_engine import BaseEngine


class AnomalyDetectionListener:
    def __init__(self, observable: Observable, anomaly_detection_engine: BaseEngine):
        self.anomaly_detection_engine = anomaly_detection_engine
        self.observable = observable
        self.time_interval = Subject()
        self.observer = AnomalyDetectionListener.AnomalyDetectionObserver(self.anomaly_detection_engine)
        self.observable.subscribe(self.time_interval)

    class AnomalyDetectionObserver(Observer):
        def __init__(self, anomaly_detection_engine: BaseEngine):
            self.anomaly_detection_engine = anomaly_detection_engine
            super(AnomalyDetectionListener.AnomalyDetectionObserver, self).__init__()

        def on_next(self, value):
            print("Hola")

        def on_error(self, error):
            pass

        def on_completed(self):
            pass
