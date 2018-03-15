import datetime


class InputMessage:
    def __init__(self, application: str, value: float, ts_str: str):
        self.ts = datetime.datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        self.value = value
        self.application = application
