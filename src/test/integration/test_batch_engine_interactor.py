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
import unittest
from collections import Generator
from datetime import datetime

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.entities.json_input_message_handler import \
    InputJsonMessageHandler
from anomalydetection.backend.interactor.batch_engine import BatchEngineInteractor
from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.common.logging import LoggingMixin


class DummyBatch(BaseStreamConsumer):

    def __init__(self) -> None:
        super().__init__()

    def poll(self) -> Generator:
        for i in range(1000):
            line = json.dumps({"application": "test",
                               "value": i,
                               "ts": str(datetime.now())})
            yield line


class TestBatchEngineInteractor(unittest.TestCase, LoggingMixin):

    def test_robust_batch_engine_interactor(self):

        interactor = BatchEngineInteractor(
            DummyBatch(),
            EngineBuilderFactory.get_robust(),
            InputJsonMessageHandler())
        data = interactor.process()

        for i, item in enumerate(data):
            self.assertEqual(item.agg_value, i)

    def test_cad_batch_engine_interactor(self):

        interactor = BatchEngineInteractor(
            DummyBatch(),
            EngineBuilderFactory.get_cad(),
            InputJsonMessageHandler())
        data = interactor.process()

        for i, item in enumerate(data):
            self.assertEqual(item.agg_value, i)
