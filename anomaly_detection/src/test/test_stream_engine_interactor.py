# -*- coding:utf-8 -*- #

import time
import unittest
from collections import Generator

from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.backend.stream import StreamBackend, MessageHandler, T, Middleware


class DummyStream(StreamBackend):

    def poll(self) -> Generator:
        for i in range(50):
            yield i
            time.sleep(2)

    def push(self, message: str) -> None:
        print(message)


class DummyMessageHandler(MessageHandler[dict]):

    @classmethod
    def parse_message(cls, message: str) -> T:
        return message

    @classmethod
    def extract_value(cls, message: T) -> float:
        return float(message)

    @classmethod
    def validate_message(cls, message: T) -> bool:
        return True


class DummyMiddleware(Middleware):

    def on_next(self, value):
        print(value)

    def on_error(self, error):
        print(error)

    def on_completed(self):
        print("Done!")


class TestStreamEngineInteractor(unittest.TestCase):

    def test(self):

        stream = DummyStream()
        engine = RobustDetector(30, 0.95)
        interactor = StreamEngineInteractor(
            stream,
            engine,
            DummyMessageHandler(),
            middleware=[DummyMiddleware()],
            agg_window_millis=5 * 1000)
        interactor.run()
