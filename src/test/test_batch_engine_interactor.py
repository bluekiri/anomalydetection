# -*- coding:utf-8 -*- #
import json
import unittest
from collections import Generator
from datetime import datetime

from anomalydetection.backend.engine.robust_z_engine import RobustDetector
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.interactor.batch_engine import \
    BatchEngineInteractor
from anomalydetection.backend.stream import \
    BasePollingStream
from test import LoggingMixin


class DummyBatch(BasePollingStream):

    def poll(self) -> Generator:
        for i in range(100):
            line = json.dumps({"application": "test",
                               "value": i,
                               "ts": str(datetime.now())})
            yield line


class TestBatchEngineInteractor(unittest.TestCase, LoggingMixin):

    def test_batch_engine_interactor(self):

        stream = DummyBatch()
        engine = RobustDetector(30, 0.98)
        interactor = BatchEngineInteractor(
            stream,
            engine,
            InputJsonMessageHandler())
        data = interactor.process()
        for i in data:
            self.logger.debug(i)

        assert True