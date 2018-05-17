# -*- coding:utf-8 -*- #
from anomalydetection.backend.entities.output_message import AnomalyResult


class BaseEngine(object):

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        raise NotImplementedError("To implement in child classes.")
