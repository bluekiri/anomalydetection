# -*- coding:utf-8 -*- #

from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.stream import \
    BaseMessageHandler, BaseObservable


class BatchEngineInteractor(object):

    def __init__(self,
                 batch: BaseObservable,
                 engine: BaseEngine,
                 message_handler: BaseMessageHandler) -> None:
        super().__init__()
        self.batch = batch
        self.engine = engine
        self.message_handler = message_handler

    def process(self) -> list:

        processed = self.batch.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: {
                "value": self.message_handler.extract_value(x),
                "ts": self.message_handler.extract_ts(x),
                "anomaly_results": self.engine.predict(
                    self.message_handler.extract_value(x)).to_dict()
            })
        return processed.to_blocking()
