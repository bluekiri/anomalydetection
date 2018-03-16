from anomalydetection.interactor.anomaly_detection_engine.base_engine import BaseEngine


class DummyEngine(BaseEngine):

    def predict(self, value: float) -> bool:
        return True
