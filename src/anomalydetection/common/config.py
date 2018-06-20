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

import logging
import os
import yaml

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.backend.middleware.store_repository_middleware import \
    StoreRepositoryMiddleware
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.builder import StreamBuilderFactory


class Config(object):

    def __init__(self,
                 mode: str = "regular",
                 yaml_stream=None) -> None:
        super().__init__()
        self.mode = mode
        self.root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        if not yaml_stream:
            if self.mode == "regular":
                try:
                    self.config = \
                        yaml.load(open(os.environ["HOME"] + "/anomdec/anomdec.yml"))
                except FileNotFoundError as e:
                    logging.info("Cannot load default configuration.")
            elif self.mode == "devel":
                self.config = yaml.load(open(self.root + "/anomdec.yml"))
        else:
            self.config = yaml.load(yaml_stream)
        self.built = None

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
            streams.append(builder.build() if builder else builder)
        return streams

    def _get_stream(self, item):
        builder = None
        backend = item["backend"]
        if backend["type"] == "kafka":
            builder = StreamBuilderFactory.get_kafka()
            builder.set_broker_server(backend["params"]["brokers"])
            builder.set_input_topic(backend["params"]["in"])
            builder.set_output_topic(backend["params"]["out"])
            if "group_id" in backend["params"]:
                builder.set_group_id(backend["params"]["group_id"])

        if backend["type"] == "pubsub":
            builder = StreamBuilderFactory.get_pubsub()
            builder.set_project_id(backend["params"]["project"])
            builder.set_subscription(backend["params"]["in"])
            builder.set_output_topic(backend["params"]["out"])
            if "auth_file" in backend["params"]:
                builder.set_auth_file(backend["params"]["auth_file"])

        if "aggregation" in item:
            agg = item["aggregation"]
            builder.set_agg_function(AggregationFunction(agg["function"]))
            builder.set_agg_window_millis(agg["window_millis"])

        return builder

    def get_engines(self):
        engines = []
        for item in self.config["streams"]:
            engines.append(self._get_engine(item["engine"]))
        return engines

    def _get_engine(self, engine):
        builder = None
        if engine["type"] == "cad":
            builder = EngineBuilderFactory.get_cad()
            if "min_value" in engine["params"]:
                builder.set_min_value(engine["params"]["min_value"])
            if "max_value" in engine["params"]:
                builder.set_max_value(engine["params"]["max_value"])
            if "rest_period" in engine["params"]:
                builder.set_rest_period(engine["params"]["rest_period"])
            if "num_norm_value_bits" in engine["params"]:
                builder.set_num_norm_value_bits(
                    engine["params"]["num_norm_value_bits"])
            if "max_active_neurons_num" in engine["params"]:
                builder.set_max_active_neurons_num(
                    engine["params"]["max_active_neurons_num"])
            if "max_left_semi_contexts_length" in engine["params"]:
                builder.set_max_left_semi_contexts_length(
                    engine["params"]["max_left_semi_contexts_length"])

        if engine["type"] == "robust":
            builder = EngineBuilderFactory.get_robust()
            if "window" in engine["params"]:
                builder.set_window(engine["params"]["window"])

        if "threshold" in engine["params"]:
            builder.set_threshold(engine["params"]["threshold"])

        return builder

    def get(self):
        if not self.built:
            self.built = list(zip(self.get_streams(),
                                  self.get_engines(),
                                  self.get_middlewares(),
                                  self.get_warmup()))
        return self.built

    def get_as_dict(self):
        keys = self.get_names()
        values = self.get()
        named = list(zip(keys, values))
        return dict((x, y) for x, y in named)

    def get_middlewares(self):
        middlewares = []
        for item in self.config["streams"]:

            if "middleware" not in item:
                middlewares.append(None)
                continue

            mid_list = []
            for mid_item in item["middleware"]:
                builder = self._get_repository(mid_item["repository"])
                if builder:
                    mid_list.append(StoreRepositoryMiddleware(builder.build()))

            middlewares.append(mid_list)

        return middlewares

    def get_warmup(self):
        warmups = []
        for item in self.config["streams"]:

            if "warmup" not in item:
                warmups.append(None)
                continue

            warmup_list = []
            for warmup_item in item["warmup"]:
                builder = self._get_repository(warmup_item["repository"])
                if builder:
                    warmup_list.append(ObservableRepository(builder.build()))

            warmups.append(warmup_list)

        return warmups

    def _get_repository(self, repository):
        builder = None
        if repository["type"] == "sqlite":
            builder = RepositoryBuilderFactory.get_sqlite()
            if "database" in repository["params"]:
                builder.set_database(repository["params"]["database"])
        return builder
