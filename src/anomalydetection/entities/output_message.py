import datetime

class OutputMessage:
    def __init__(self, application: str, anomaly_provability: float, ts: datetime):
        self.ts = ts
        self.anomaly_provability = anomaly_provability
        self.application = application
