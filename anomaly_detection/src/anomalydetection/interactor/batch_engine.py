# -*- coding:utf-8 -*- #

from rx import Observable

from anomalydetection.engine.base_engine import BaseEngine
from anomalydetection.stream import StreamBackend, MessageHandler


class BatchEngineInteractor(object):

    def __init__(self,
                 batch: StreamBackend,
                 engine: BaseEngine,
                 message_handler: MessageHandler) -> None:
        super().__init__()
        self.batch = batch
        self.engine = engine
        self.message_handler = message_handler

    def process(self) -> list:

        processed = Observable.from_(self.batch.poll()) \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: {
                "value": self.message_handler.extract_value(x),
                "ts": self.message_handler.extract_ts(x),
                "anomaly_results": self.engine.predict(
                    self.message_handler.extract_value(x)).to_dict()
            })
        return processed.to_blocking()
