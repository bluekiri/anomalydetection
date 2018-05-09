# -*- coding:utf-8 -*- #

from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.stream import \
    BaseObservable


class BatchEngineInteractor(object):

    def __init__(self,
                 batch: BaseObservable,
                 engine: BaseEngine,
                 message_handler: BaseMessageHandler) -> None:
        super().__init__()
        self.batch = batch
        self.engine = engine
        self.message_handler = message_handler

    def build_output_message(self, message):
        extra_values = self.message_handler.extract_extra(message)
        anomaly_results = self.engine.predict(
                self.message_handler.extract_value(message), **extra_values)
        params = {
            "application": message.application,
            "agg_value": message.value,
            "agg_function": None,
            "agg_window_millis": None,
            "ts": message.ts,
            "anomaly_results": anomaly_results
        }
        return OutputMessage(**params)

    def process(self) -> list:

        processed = self.batch.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: self.build_output_message(x))
        return processed.to_blocking()
