# -*- coding:utf-8 -*-
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
import importlib
import uuid

from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.backend.stream import BaseStreamProducer
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.kafka import KafkaStreamConsumer
from anomalydetection.backend.stream.kafka import KafkaStreamProducer
from anomalydetection.backend.stream.kafka import SparkKafkaStreamConsumer
from anomalydetection.backend.stream.pubsub import PubSubStreamConsumer
from anomalydetection.backend.stream.pubsub import SparkPubsubStreamConsumer
from anomalydetection.backend.stream.pubsub import PubSubStreamProducer


class BaseConsumerBuilder(object):

    def build(self) -> BaseStreamConsumer:
        raise NotImplementedError("To implement in child classes.")

    def set(self, name: str, value: str):
        def raise_exception(*args, **kwargs):
            raise NotImplementedError()
        func_name = "set_{}".format(name)
        func = getattr(self, func_name, raise_exception)
        try:
            return func(value)
        except NotImplementedError as ex:
            raise NotImplementedError(
                "Calling undefined function: {}.{}()".format(
                    self.__class__.__name__, func_name))


class BaseProducerBuilder(object):

    def build(self) -> BaseStreamProducer:
        raise NotImplementedError("To implement in child classes.")

    def set(self, name: str, value: str):
        def raise_exception(*args, **kwargs):
            raise NotImplementedError()
        func_name = "set_{}".format(name)
        func = getattr(self, func_name, raise_exception)
        try:
            return func(value)
        except NotImplementedError as ex:
            raise NotImplementedError(
                "Calling undefined function: {}.{}()".format(
                    self.__class__.__name__, func_name))


class KafkaStreamConsumerBuilder(BaseConsumerBuilder):

    def __init__(self,
                 broker_servers: str = None,
                 input_topic: str = None,
                 group_id: str = str(uuid.uuid4()),
                 agg_function: AggregationFunction = AggregationFunction.NONE,
                 agg_window_millis: int = 0) -> None:
        super().__init__()
        self.broker_servers = broker_servers
        self.input_topic = input_topic
        self.group_id = group_id
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def set_broker_servers(self, broker_servers):
        self.broker_servers = broker_servers
        return self

    def set_input_topic(self, input_topic):
        self.input_topic = input_topic
        return self

    def set_group_id(self, group_id):
        self.group_id = group_id
        return self

    def set_agg_function(self, agg_function: AggregationFunction):
        if isinstance(agg_function, str):
            agg_function = AggregationFunction(agg_function)
        self.agg_function = agg_function
        return self

    def set_agg_window_millis(self, agg_window_millis: int):
        self.agg_window_millis = agg_window_millis
        return self

    def build(self) -> BaseStreamConsumer:
        if self.agg_function and self.agg_function != AggregationFunction.NONE:
            return SparkKafkaStreamConsumer(**vars(self).copy())
        else:
            args = vars(self).copy()
            del args["agg_function"]
            del args["agg_window_millis"]
            return KafkaStreamConsumer(**args)

    def __str__(self) -> str:
        return "Kafka topic: " \
               "brokers: {}, topic: {}, func: {}, window: {}ms".format(
                    self.broker_servers,
                    self.input_topic,
                    self.agg_function,
                    self.agg_window_millis)


class KafkaStreamProducerBuilder(BaseProducerBuilder):

    def __init__(self,
                 broker_servers: str = None,
                 output_topic: str = None) -> None:
        super().__init__()
        self.broker_servers = broker_servers
        self.output_topic = output_topic

    def set_broker_servers(self, broker_servers):
        self.broker_servers = broker_servers
        return self

    def set_output_topic(self, output_topic):
        self.output_topic = output_topic
        return self

    def build(self) -> BaseStreamProducer:
        return KafkaStreamProducer(**vars(self).copy())


class PubSubStreamConsumerBuilder(BaseConsumerBuilder):

    def __init__(self,
                 project_id: str = None,
                 subscription: str = None,
                 auth_file: str = None,
                 agg_function: AggregationFunction = AggregationFunction.NONE,
                 agg_window_millis: int = 0) -> None:
        super().__init__()
        self.project_id = project_id
        self.subscription = subscription
        self.auth_file = auth_file
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def set_project_id(self, project_id):
        self.project_id = project_id
        return self

    def set_subscription(self, subscription):
        self.subscription = subscription
        return self

    def set_auth_file(self, auth_file: str):
        self.auth_file = auth_file
        return self

    def set_agg_function(self, agg_function: AggregationFunction):
        if isinstance(agg_function, str):
            agg_function = AggregationFunction(agg_function)
        self.agg_function = agg_function
        return self

    def set_agg_window_millis(self, agg_window_millis: int):
        self.agg_window_millis = agg_window_millis
        return self

    def build(self) -> BaseStreamConsumer:
        if self.agg_function and self.agg_function != AggregationFunction.NONE:
            return SparkPubsubStreamConsumer(**vars(self).copy())
        else:
            args = vars(self).copy()
            del args["agg_function"]
            del args["agg_window_millis"]
            return PubSubStreamConsumer(**args)

    def __str__(self) -> str:
        return "PubSub subscription: " \
               "project: {}, subscription: {}, func: {}, window: {}ms".format(
                    self.project_id,
                    self.subscription,
                    self.agg_function,
                    self.agg_window_millis)


class PubSubStreamProducerBuilder(BaseProducerBuilder):

    def __init__(self,
                 project_id: str = None,
                 output_topic: str = None,
                 auth_file: str = None) -> None:
        super().__init__()
        self.project_id = project_id
        self.output_topic = output_topic
        self.auth_file = auth_file

    def set_project_id(self, project_id):
        self.project_id = project_id
        return self

    def set_output_topic(self, output_topic):
        self.output_topic = output_topic
        return self

    def set_auth_file(self, auth_file: str):
        self.auth_file = auth_file
        return self

    def build(self) -> BaseStreamProducer:
        return PubSubStreamProducer(**vars(self).copy())


class StreamBuilderFactory(object):

    @staticmethod
    def get_consumer_plugin(name) -> BaseConsumerBuilder:
        module_name = "anomalydetection.backend.stream.{}_builder".format(name)
        objects = vars(importlib.import_module(module_name))["_objects"]
        for obj in objects:
            if issubclass(obj, BaseConsumerBuilder):
                return obj()
        raise NotImplementedError()

    @staticmethod
    def get_consumer(name) -> BaseConsumerBuilder:
        def raise_exception():
            raise NotImplementedError()
        func_name = "get_consumer_{}".format(name)
        func = getattr(StreamBuilderFactory, func_name, raise_exception)
        try:
            return func()
        except NotImplementedError as ex:
            try:
                return StreamBuilderFactory.get_consumer_plugin(name)
            except NotImplementedError as ex:
                raise NotImplementedError(
                    "Calling undefined function: {}.{}()".format(
                        "EngineBuilderFactory", func_name))

    @staticmethod
    def get_producer_plugin(name) -> BaseProducerBuilder:
        module_name = "anomalydetection.backend.stream.{}_builder".format(name)
        objects = vars(importlib.import_module(module_name))["_objects"]
        for obj in objects:
            if issubclass(obj, BaseProducerBuilder):
                return obj()
        raise NotImplementedError()

    @staticmethod
    def get_producer(name) -> BaseProducerBuilder:
        def raise_exception():
            raise NotImplementedError()
        func_name = "get_producer_{}".format(name)
        func = getattr(StreamBuilderFactory, func_name, raise_exception)
        try:
            return func()
        except NotImplementedError as ex:
            try:
                return StreamBuilderFactory.get_producer_plugin(name)
            except NotImplementedError as ex:
                raise NotImplementedError(
                    "Calling undefined function: {}.{}()".format(
                        "StreamBuilderFactory", func_name))

    @staticmethod
    def get_consumer_kafka():
        return KafkaStreamConsumerBuilder()

    @staticmethod
    def get_producer_kafka():
        return KafkaStreamProducerBuilder()

    @staticmethod
    def get_consumer_pubsub():
        return PubSubStreamConsumerBuilder()

    @staticmethod
    def get_producer_pubsub():
        return PubSubStreamProducerBuilder()
