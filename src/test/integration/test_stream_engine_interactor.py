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

import datetime
import unittest
from collections import Generator

from rx import Observable

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor.stream_engine import StreamEngineInteractor
from anomalydetection.backend.sink import BaseSink
from anomalydetection.backend.stream import BaseStreamConsumer, BaseObservable
from anomalydetection.backend.stream.builder import BaseConsumerBuilder
from anomalydetection.common.logging import LoggingMixin


class DummyStream(BaseStreamConsumer, LoggingMixin):

    def poll(self) -> Generator:
        for i in range(5):
            yield i

    def push(self, message: str) -> None:
        self.logger.debug("Pushing message: {}".format(message))


class DummyStreamBuilder(BaseConsumerBuilder):

    def build(self) -> BaseStreamConsumer:
        return DummyStream()


class DummyMessageHandler(BaseMessageHandler[InputMessage]):

    @classmethod
    def parse_message(cls, message: str) -> InputMessage:
        return InputMessage("app",
                            float(message),
                            datetime.datetime.now())

    @classmethod
    def extract_key(cls, message: InputMessage) -> str:
        return message.application

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        return True

    @classmethod
    def extract_extra(cls, message: InputMessage) -> dict:
        return {"ts": message.ts}


class DummySink(BaseSink, LoggingMixin):

    def on_next(self, value):
        self.logger.debug("Middleware on_next: {}".format(value))

    def on_error(self, error):
        self.logger.debug("Middleware on_error: {}".format(error))

    def on_completed(self):
        self.logger.debug("Middleware on_completed.")


class DummyWarmUp(BaseObservable, LoggingMixin):

    def dummy_generator(self) -> Generator:
        for i in range(50):
            yield OutputMessage("app", None, None, None,
                                i, datetime.datetime.now())

    def get_observable(self):
        return Observable.from_(self.dummy_generator())


class TestStreamEngineInteractor(unittest.TestCase, LoggingMixin):

    def test_robust_stream_engine_interactor(self):

        interactor = StreamEngineInteractor(
            DummyStreamBuilder(),
            EngineBuilderFactory.get_robust().set_window(30).set_threshold(.95),
            DummyMessageHandler(),
            sinks=[DummySink()],
            warm_up=DummyWarmUp())
        interactor.run()

    def test_cad_stream_engine_interactor(self):

        interactor = StreamEngineInteractor(
            DummyStreamBuilder(),
            EngineBuilderFactory.get_cad(),
            DummyMessageHandler(),
            sinks=[DummySink()],
            warm_up=DummyWarmUp())
        interactor.run()
