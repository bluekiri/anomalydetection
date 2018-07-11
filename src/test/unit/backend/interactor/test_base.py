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

import unittest
from typing import Any

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.interactor import BaseEngineInteractor
from anomalydetection.backend.stream import BaseObservable


class TestBaseWarmUp(unittest.TestCase):

    def test_constructor(self):
        BaseObservable()


class DummyEngine(BaseEngine):

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        return AnomalyResult(-10, 10, 0.5, False)


class DummyEngineBuilder(BaseEngineBuilder):

    def build(self) -> BaseEngine:
        return DummyEngine()


class DummyMessageHandler(BaseMessageHandler):

    @classmethod
    def parse_message(cls, message: str) -> dict:
        return dict(key="key", value=1)

    @classmethod
    def extract_key(cls, message: dict) -> str:
        return message["key"]

    @classmethod
    def extract_value(cls, message: dict) -> Any:
        return message["value"]

    @classmethod
    def validate_message(cls, message: dict) -> bool:
        return True


class TestBaseEngineInteractor(unittest.TestCase):

    def test_constructor(self):
        interactor = BaseEngineInteractor(DummyEngineBuilder(),
                                          DummyMessageHandler())
        self.assertIsInstance(interactor.engine_builder, DummyEngineBuilder)
        self.assertIsInstance(interactor.message_handler, DummyMessageHandler)
        self.assertDictEqual(interactor.app_engine, {})

    def test_get_engine(self):
        interactor = BaseEngineInteractor(DummyEngineBuilder(),
                                          DummyMessageHandler())
        self.assertIsInstance(interactor.get_engine("any"),
                              DummyEngine)
