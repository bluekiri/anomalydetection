# -*- coding:utf-8 -*- #
import datetime
import time
import unittest
from collections import Generator

from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import WarmUp
from anomalydetection.backend.interactor.stream_engine import \
    StreamEngineInteractor
from anomalydetection.backend.store_middleware import Middleware
from anomalydetection.backend.stream import BaseStreamBackend
from rx import Observable


class DummyStream(BaseStreamBackend):

    def poll(self) -> Generator:
        for i in range(5):
            yield i
            time.sleep(2)

    def push(self, message: str) -> None:
        print(message)


class DummyMessageHandler(BaseMessageHandler[InputMessage]):

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


class DummyMiddleware(Middleware):

    def on_next(self, value):
        print(value)

    def on_error(self, error):
        print(error)

    def on_completed(self):
        print("Done!")


class DummyWarmUp(WarmUp):

    def dummy_generator(self) -> Generator:
        for i in range(50):
            yield OutputMessage("app", None, None, None,
                                i, datetime.datetime.now())

    def get_observable(self):
        return Observable.from_(self.dummy_generator())


class TestStreamEngineInteractor(unittest.TestCase):

    def test(self):

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
