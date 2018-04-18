# -*- coding:utf-8 -*- #
import json
import os
import unittest
from collections import Generator
from datetime import datetime

from anomalydetection.engine.robust_z_engine import RobustDetector
from anomalydetection.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.stream import StreamBackend, MessageHandler, T, BatchBase


class DummyBatch(BatchBase):

    def poll(self) -> Generator:
        with open(os.getenv("HOME") + "/anom-detection-predictions.json") as f:
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    break


class InputJsonHandler(MessageHandler[dict]):

    @classmethod
    def extract_ts(cls, message: dict) -> datetime:
        return message["ts"]

    @classmethod
    def parse_message(cls, message: str) -> T:
        return json.loads(message)

    @classmethod
    def extract_value(cls, message: dict) -> float:
        return message["agg_value"]

    @classmethod
    def validate_message(cls, message: dict) -> bool:
        return True


class TestBatchEngineInteractor(unittest.TestCase):

    def test(self):

        stream = DummyBatch()
        engine = RobustDetector(30, 0.98)
        interactor = BatchEngineInteractor(
            stream,
            engine,
            InputJsonHandler())
        data = interactor.process()
        for i in data:
            print(i)
