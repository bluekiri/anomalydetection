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
from typing import List, Any, Iterable, Generator

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage, AnomalyResult
from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.builder import BaseRepositoryBuilder
from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.backend.stream import BaseStreamProducer
from anomalydetection.backend.stream.builder import BaseConsumerBuilder
from anomalydetection.backend.stream.builder import BaseProducerBuilder
from anomalydetection.common.plugins import Plugin


class PluginOneRepository(BaseRepository):

    def initialize(self):
        pass

    def fetch(self, application, from_ts, to_ts) -> Iterable:
        pass

    def insert(self, message: OutputMessage) -> None:
        pass

    def map(self, item: Any) -> OutputMessage:
        pass

    def get_applications(self) -> List[str]:
        pass


class PluginOneRepositoryBuilder(BaseRepositoryBuilder):

    def build(self) -> BaseRepository:
        return PluginOneRepository("plugin1")


class EngineOne(BaseEngine):

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        return AnomalyResult(-1, 1, 0, False)


class EngineOneBuilder(BaseEngineBuilder):

    type = "plugin1"

    def build(self) -> BaseEngine:
        return EngineOne()


class ConsumerOne(BaseStreamConsumer):

    def poll(self) -> Generator:
        yield 1


class ConsumerOneBuilder(BaseConsumerBuilder):

    def build(self) -> BaseStreamConsumer:
        return ConsumerOne()


class ProducerOne(BaseStreamProducer):

    def push(self, message: str) -> None:
        pass


class ProducerOneBuilder(BaseProducerBuilder):

    def build(self) -> BaseStreamProducer:
        return ProducerOne()


class HandlerOne(BaseMessageHandler[InputMessage]):

    @classmethod
    def parse_message(cls, message: Any) -> InputMessage:
        pass

    @classmethod
    def extract_key(cls, message: InputMessage) -> str:
        pass

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        pass

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        pass


class PluginOneRepositoryPlugin(Plugin):
    name = "plugin1"
    stream_consumer_builders = [ConsumerOneBuilder]
    stream_consumers = [ConsumerOne]
    stream_producer_builders = [ProducerOneBuilder]
    stream_producers = [ProducerOne]
    repositories = [PluginOneRepository]
    repository_builders = [PluginOneRepositoryBuilder]
    engines = [EngineOne]
    engine_builders = [EngineOneBuilder]
    message_handlers = [HandlerOne]
