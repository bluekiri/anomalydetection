# -*- coding:utf-8 -*- #

import time
import unittest
from collections import Generator
from random import randint

from anomalydetection.interactor.engine.robust_z_engine import RobustDetector
from anomalydetection.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.stream import StreamBackend, MessageHandler, T


class DummyStream(StreamBackend):

    def poll(self) -> Generator:
        for i in range(1000):
            yield randint(0, 1000)
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


class TestStreamEngineInteractor(unittest.TestCase):

    def test(self):

        stream = DummyStream()
        engine = RobustDetector(30, 0.95)
        interactor = StreamEngineInteractor(
            stream,
            engine,
            DummyMessageHandler(),
            agg_window=5 * 1000)
        interactor.run()
