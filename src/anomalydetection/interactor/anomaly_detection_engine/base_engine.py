class BaseEngine:

    def predict(self, value: float) -> bool:
        raise NotImplementedError()