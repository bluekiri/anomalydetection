# -*- coding:utf-8 -*- #

import logging
import os
import yaml

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.backend.store_middleware.store_repository_middleware import \
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

    def get_streams(self):
        streams = []
        for item in self.config["streams"]:
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

            if builder:
                streams.append(builder.build())
            else:
                streams.append(builder)

        return streams

    def get_engines(self):
        engines = []
        for item in self.config["streams"]:
            builder = None
            engine = item["engine"]
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

            engines.append(builder)

        return engines

    def get(self):
        if not self.built:
            self.built = list(zip(self.get_streams(),
                                  self.get_engines(),
                                  self.get_middlewares(),
                                  self.get_warmup()))
        return self.built

    def get_as_dict(self):
        names = self.get_names()
        other = self.get()
        named = list(zip(names, other))
        return dict((x, y) for x, y in named)

    def build_publishers(self):
        config = Config(self.mode)
        for item in config.config["streams"]:
            if "aggregation" in item:
                del item["aggregation"]

        for item in config.config["streams"]:

            # Flip topics
            topic = item["backend"]["params"]["in"]
            item["backend"]["params"]["in"] = "deleted"
            item["backend"]["params"]["out"] = topic

            # Topic is not auto created in PubSub
            if item["backend"]["type"] == "pubsub":
                project = item["backend"]["params"]["project"]
                try:
                    publisher = PublisherClient()
                    publisher.create_topic(
                        publisher.topic_path(project,
                                             topic))

                    subscriber = SubscriberClient()
                    subscriber.create_subscription(
                        subscriber.subscription_path(project, topic),
                        subscriber.topic_path(project, topic))
                except AlreadyExists as _:
                    pass

        streams = config.get_streams()
        return streams

    def get_middlewares(self):
        middlewares = []
        for item in self.config["streams"]:

            if "middleware" not in item:
                middlewares.append(None)
                continue

            builder = None
            mid_list = []
            for mid_item in item["middleware"]:
                repository = mid_item["repository"]
                if repository["type"] == "sqlite":
                    builder = RepositoryBuilderFactory.get_sqlite()
                    if "database" in repository["params"]:
                        builder.set_database(repository["params"]["database"])

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

            builder = None
            warmup_list = []
            for warmup_item in item["warmup"]:
                repository = warmup_item["repository"]
                if repository["type"] == "sqlite":
                    builder = RepositoryBuilderFactory.get_sqlite()
                    if "database" in repository["params"]:
                        builder.set_database(repository["params"]["database"])

                if builder:
                    warmup_list.append(ObservableRepository(builder.build()))

            warmups.append(warmup_list)

        return warmups
