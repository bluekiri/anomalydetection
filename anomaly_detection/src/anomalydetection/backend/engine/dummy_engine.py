from anomalydetection.backend.engine.base_engine import BaseEngine


class DummyEngine(BaseEngine):

    def predict(self, value: float) -> float:
        return 1.0
