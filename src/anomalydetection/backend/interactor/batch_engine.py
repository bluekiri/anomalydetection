# -*- coding:utf-8 -*- #
import logging

from anomalydetection.backend.engine.builder import BaseBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import BaseEngineInteractor
from anomalydetection.backend.stream import BaseObservable


class BatchEngineInteractor(BaseEngineInteractor):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self,
                 batch: BaseObservable,
                 engine_builder: BaseBuilder,
                 message_handler: BaseMessageHandler) -> None:
        super().__init__(engine_builder, message_handler)
        self.batch = batch
        self.app_engine = {}

    def map_with_engine(self, input_message: InputMessage) -> OutputMessage:
        key = self.message_handler.extract_key(input_message)
        value = self.message_handler.extract_value(input_message)
        extra_values = self.message_handler.extract_extra(input_message)

        anomaly_results = \
            self.get_engine(key) \
                .predict(value, **extra_values)

        ts = self.message_handler.extract_ts(input_message)
        output = {
            "application": input_message.application,
            "agg_value": value,
            "agg_function": None,
            "agg_window_millis": None,
            "ts": ts,
            "anomaly_results": anomaly_results
        }
        return OutputMessage(**output)

    def process(self) -> list:

        processed = self.batch.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: self.map_with_engine(x))
        return processed.to_blocking()
