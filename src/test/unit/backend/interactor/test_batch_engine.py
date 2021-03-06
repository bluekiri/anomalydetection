# -*- coding:utf-8 -*- #
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import math
import unittest
from collections import Generator
from datetime import datetime
from typing import Any

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.common.logging import LoggingMixin


class DummyBatch(BaseStreamConsumer):

    def __init__(self) -> None:
        super().__init__()

    def poll(self) -> Generator:
        for i in range(10):
            line = json.dumps({"application": "test",
                               "value": i,
                               "ts": str(datetime.now())})
            yield line


class DummyEngine(BaseEngine):

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        return AnomalyResult(-10 * value, 10 * value,
                             math.pow(value, 0.5), bool(value % 2))


class DummyEngineBuilder(BaseEngineBuilder):

    def build(self) -> BaseEngine:
        return DummyEngine()


class DummyMessageHandler(BaseMessageHandler):

    @classmethod
    def parse_message(cls, message: str) -> dict:
        return json.loads(message)

    @classmethod
    def extract_key(cls, message: dict) -> str:
        return message["application"]

    @classmethod
    def extract_value(cls, message: dict) -> Any:
        return message["value"]

    @classmethod
    def validate_message(cls, message: dict) -> bool:
        return True


class TestBatchEngineInteractor(unittest.TestCase, LoggingMixin):

    def test_batch_engine_interactor(self):

        interactor = BatchEngineInteractor(
            DummyBatch(),
            DummyEngineBuilder(),
            DummyMessageHandler())

        for i, item in enumerate(interactor.process()):
            self.assertEqual(item.agg_value, i)
            self.assertEqual(item.anomaly_results,
                             AnomalyResult(-10 * i, 10 * i,
                                           math.pow(i, 0.5), bool(i % 2)))
