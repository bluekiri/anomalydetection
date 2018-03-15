class BaseEngine:

    def __init__(self, windows_in_seconds: int):
        self.windows_in_seconds = windows_in_seconds

    def predict(self, value: float):
        raise NotImplementedError()
