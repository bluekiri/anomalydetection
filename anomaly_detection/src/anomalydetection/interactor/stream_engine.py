# -*- coding:utf-8 -*- #

import json
from typing import Any, List

from anomalydetection.entities.input_message import InputMessage
from anomalydetection.entities.output_message import OutputMessage
from rx import Observable

from anomalydetection.engine.base_engine import BaseEngine
from anomalydetection.stream import StreamBackend, MessageHandler, Middleware


class StreamEngineInteractor(object):

    DEFAULT_AGG_WINDOW = 5 * 60 * 1000
    DEFAULT_AGG_FUNCTION = sum

    def __init__(self,
                 stream: StreamBackend,
                 engine: BaseEngine,
                 message_handler: MessageHandler,
                 middleware: List[Middleware] = [],
                 agg_function: callable = DEFAULT_AGG_FUNCTION,
                 agg_window_millis: int = DEFAULT_AGG_WINDOW) -> None:
        super().__init__()
        self.stream = stream
        self.engine = engine
        self.middleware = middleware
        self.message_handler = message_handler
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def build_output_message(self, value):
        input_message, agg_value = value
        output = {
            "application": input_message.application,
            "agg_value": agg_value,
            "agg_function": str(self.agg_function),
            "agg_window_millis": self.agg_window_millis,
            "ts": str(self.message_handler.extract_ts(input_message)),
            "anomaly_results": self.engine.predict(agg_value)
        }
        return OutputMessage(**output)

    def zip_input_with_agg(self, value):
        return (
            value[-1],
            self.agg_function(
                map(self.message_handler.extract_value, value))
        )

    def run(self):

        # Aggregate and map input values.
        stream = Observable.from_(self.stream.poll()) \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \

        rx = stream \
            .buffer_with_time(timespan=self.agg_window_millis) \
            .filter(lambda x: x) \
            .map(lambda x: self.zip_input_with_agg(x)) \
            .map(lambda x: self.build_output_message(x)) \
            .publish()  # This is required for multiple subscriptions

        # Main subscription
        rx.subscribe(lambda x: self.stream.push(str(x)))

        # Middleware
        for mw in self.middleware:
            rx.subscribe(mw)

        # Connect with observers
        rx.connect()
