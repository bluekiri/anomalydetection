# -*- coding:utf-8 -*- #
import datetime
import json

from rx import Observable

from anomalydetection.engine.base_engine import BaseEngine
from anomalydetection.stream import StreamBackend, MessageHandler


class StreamEngineInteractor(object):

    DEFAULT_AGG_WINDOW = 5 * 60 * 1000
    DEFAULT_AGG_FUNCTION = sum

    def __init__(self,
                 stream: StreamBackend,
                 engine: BaseEngine,
                 message_handler: MessageHandler,
                 agg_function: callable = DEFAULT_AGG_FUNCTION,
                 agg_window: int = DEFAULT_AGG_WINDOW) -> None:
        super().__init__()
        self.stream = stream
        self.engine = engine
        self.message_handler = message_handler
        self.agg_function = agg_function
        self.agg_window = agg_window

    async def _do_poll(self, generator):
        for item in generator:
            return item

    def run(self):

        Observable.from_(self.stream.poll()) \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: self.message_handler.extract_value(x)) \
            .buffer_with_time(timespan=self.agg_window) \
            .filter(lambda x: len(x) > 0) \
            .map(lambda x: self.agg_function(x)) \
            .map(lambda x: {
                "agg_value": x,
                "agg_function": str(self.agg_function),
                "agg_window_millis": self.agg_window,
                "ts": datetime.datetime.now().isoformat(),
                "anomaly_results": self.engine.predict(x)
            }) \
            .subscribe(lambda x: self.stream.push(json.dumps(x)))
