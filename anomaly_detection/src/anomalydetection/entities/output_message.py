# -*- coding:utf-8 -*- #

import datetime
import json


class AnomalyResult(object):

    def __init__(self,
                 value_lower_limit: float,
                 value_upper_limit: float,
                 anomaly_probability: float,
                 is_anomaly: bool) -> None:
        super().__init__()
        self.value_lower_limit = value_lower_limit
        self.value_upper_limit = value_upper_limit
        self.anomaly_probability = anomaly_probability
        self.is_anomaly = is_anomaly

    def to_dict(self):
        return dict(value_lower_limit=self.value_lower_limit,
                    value_upper_limit=self.value_upper_limit,
                    anomaly_probability=self.anomaly_probability,
                    is_anomaly=self.is_anomaly)


class OutputMessage(object):

    def __init__(self,
                 application: str,
                 anomaly_results: AnomalyResult,
                 agg_window_millis: int,
                 agg_function: callable,
                 agg_value: float,
                 ts: datetime):
        self.application = application
        self.anomaly_results = anomaly_results
        self.agg_window_millis = agg_window_millis
        self.agg_function = agg_function
        self.agg_value = agg_value
        self.ts = ts

    def to_dict(self):
        return dict(application=self.application,
                    anomaly_results=self.anomaly_results.to_dict(),
                    agg_window_millis=self.agg_window_millis,
                    agg_function=self.agg_function,
                    agg_value=self.agg_value,
                    ts=self.ts)

    def __str__(self):
        response = self.to_dict()
        response["ts"] = str(response["ts"])  # Datetime to string
        return json.dumps(response)
