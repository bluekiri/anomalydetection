# -*- coding:utf-8 -*- #
import datetime
import logging
import time
import unittest
from collections import Generator

from rx import Observable

from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import WarmUp
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor
from anomalydetection.backend.store_middleware import Middleware
from anomalydetection.backend.stream import BaseStreamBackend
from test import LoggingMixin

logging.basicConfig()
logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)


class DummyStream(BaseStreamBackend, LoggingMixin):

    def poll(self) -> Generator:
        for i in range(5):
            yield i
            time.sleep(2)

    def push(self, message: str) -> None:
        self.logger.debug("Pushing message: {}".format(message))


class DummyMessageHandler(BaseMessageHandler[InputMessage], LoggingMixin):

    @classmethod
    def parse_message(cls, message: str) -> InputMessage:
        return InputMessage("app",
                            float(message),
                            datetime.datetime.now())

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        return True


class DummyMiddleware(Middleware, LoggingMixin):

    def on_next(self, value):
        self.logger.debug("Middleware on_next: {}".format(value))

    def on_error(self, error):
        self.logger.debug("Middleware on_error: {}".format(error))

    def on_completed(self):
        self.logger.debug("Middleware on_completed.")


class DummyWarmUp(WarmUp, LoggingMixin):

    def dummy_generator(self) -> Generator:
        for i in range(50):
            yield OutputMessage("app", None, None, None,
                                i, datetime.datetime.now())

    def get_observable(self):
        return Observable.from_(self.dummy_generator())


class TestStreamEngineInteractor(unittest.TestCase, LoggingMixin):

    def test_stream_engine_interactor(self):

        stream = DummyStream()
        engine = RobustDetector(30, 0.95)
        interactor = StreamEngineInteractor(
            stream,
            engine,
            DummyMessageHandler(),
            middleware=[DummyMiddleware()],
            warm_up=DummyWarmUp(),
            agg_window_millis=5 * 1000)
        interactor.run()
