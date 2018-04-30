# -*- coding:utf-8 -*- #
import json
import os
import unittest
from collections import Generator
from datetime import datetime

from anomalydetection.backend.entities import BaseMessageHandler, T
from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.json_input_message_handler import InputJsonMessageHandler
from anomalydetection.backend.interactor.batch_engine import \
    BatchEngineInteractor
from anomalydetection.backend.stream import \
    BasePollingStream


class DummyBatch(BasePollingStream):

    def poll(self) -> Generator:
        for i in range(100):
            line = json.dumps({"application": "test", "value": i, "ts": str(datetime.now())})
            yield line


class TestBatchEngineInteractor(unittest.TestCase):

    def test(self):

        stream = DummyBatch()
        engine = RobustDetector(30, 0.98)
        interactor = BatchEngineInteractor(
            stream,
            engine,
            InputJsonMessageHandler())
        data = interactor.process()
        for i in data:
            print(i)
