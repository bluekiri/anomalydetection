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

import os

from anomalydetection.backend.entities.handlers.factory import MessageHandlerFactory
from anomalydetection.common.logging import LoggingMixin
import yaml

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.backend.sink import BaseSink
from anomalydetection.backend.sink.repository import RepositorySink
from anomalydetection.backend.sink.stream import StreamSink
from anomalydetection.backend.stream.builder import StreamBuilderFactory


class Config(LoggingMixin):

    def __init__(self,
                 mode: str = "regular",
                 yaml_stream=None) -> None:
        super().__init__()
        self.built = None
        self.mode = mode
        self.root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.home = os.getenv("ANOMDEC_HOME", os.environ["HOME"] + "/anomdec")
        if not yaml_stream:
            if self.mode == "regular":
                try:
                    self.config = \
                        yaml.load(open("{}/anomdec.yml".format(self.home)))
                except FileNotFoundError as e:
                    self.logger.warning("Cannot load configuration. \n{}".format(str(e)))
            elif self.mode == "devel":
                self.config = yaml.load(open(self.root + "/anomdec.yml"))
        else:
            self.config = yaml.load(yaml_stream)

    def get_names(self):
        streams = []
        for item in self.config["streams"]:
            streams.append(item["name"])

        return streams

    def get_websocket_url(self):
        return self.config["websocket"]

    def get_streams(self):
        streams = []
        for item in self.config["streams"]:
            builder = self._get_stream(item)
            streams.append(builder if builder else builder)
        return streams

    def _get_stream(self, item):
        source = item["source"]
        builder = StreamBuilderFactory.get_consumer(source["type"])
        params = source["params"] if "params" in source else {}
        for param in params:
            builder.set(param, params[param])
        if "aggregation" in item:
            agg_params = item["aggregation"]
            for agg_param in agg_params:
                builder.set(agg_param, agg_params[agg_param])
        return builder

    def get_engines(self):
        engines = []
        for item in self.config["streams"]:
            engines.append(self._get_engine(item["engine"]))
        return engines

    def get_handlers(self):
        handlers = []
        for item in self.config["streams"]:
            try:
                handlers.append(MessageHandlerFactory.get(item["handler"]))
            except KeyError as key_error:
                handlers.append(MessageHandlerFactory.get_json())
        return handlers

    def _get_engine(self, engine):
        builder = EngineBuilderFactory.get(engine["type"])
        params = engine["params"] if "params" in engine else {}
        for param in params:
            builder.set(param, params[param])
        return builder

    def get(self):
        if not self.built:
            self.built = list(zip(self.get_streams(),
                                  self.get_handlers(),
                                  self.get_engines(),
                                  self.get_sinks(),
                                  self.get_warmup()))
        return self.built

    def get_as_dict(self):
        keys = self.get_names()
        values = self.get()
        named = list(zip(keys, values))
        return dict((x, y) for x, y in named)

    def get_sinks(self):
        sinks = []
        for item in self.config["streams"]:

            if "sink" not in item:
                sinks.append([])
                continue

            mid_list = []
            for mid_item in item["sink"]:
                builder = self._get_sink(mid_item)
                if builder:
                    mid_list.append(builder)

            sinks.append(mid_list)

        return sinks

    def get_warmup(self):
        warmups = []
        for item in self.config["streams"]:

            if "warmup" not in item:
                warmups.append([])
                continue

            warmup_list = []
            for warmup_item in item["warmup"]:
                builder = self._get_repository(warmup_item["repository"])
                if builder:
                    warmup_list.append(ObservableRepository(builder.build()))

            warmups.append(warmup_list)

        return warmups

    def _get_repository(self, repository):
        builder = RepositoryBuilderFactory.get(repository["type"])
        params = repository["params"] if "params" in repository else {}
        for param in params:
            builder.set(param, params[param])
        return builder

    def _get_sink(self, sink) -> BaseSink:
        if sink["type"] == "repository":
            builder = self._get_repository(sink["repository"])
            if builder:
                return RepositorySink(builder.build())
        if sink["type"] == "stream":
            stream = sink["stream"]
            builder = StreamBuilderFactory.get_producer(stream["type"])
            params = stream["params"] if "params" in stream else {}
            for param in params:
                builder.set(param, params[param])
            return StreamSink(builder.build())
