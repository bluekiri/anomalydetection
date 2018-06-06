# -*- coding:utf-8 -*-
import uuid

from anomalydetection.backend.stream import BaseStreamBackend
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream.kafka_stream_backend import \
    KafkaStreamBackend, SparkKafkaStreamBackend
from anomalydetection.backend.stream.pubsub_stream_backend import \
    PubSubStreamBackend


class BaseBuilder(object):

    def build(self) -> BaseStreamBackend:
        raise NotImplementedError("To implement on child classes.")


class KafkaStreamBuilder(BaseBuilder):

    def __init__(self,
                 broker_server: str = None,
                 input_topic: str = None,
                 output_topic: str = None,
                 group_id: str = str(uuid.uuid4()),
                 agg_function: AggregationFunction = None,
                 agg_window_millis: int = 0) -> None:
        super().__init__()
        self.broker_server = broker_server
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def set_broker_server(self, broker_server):
        self.broker_server = broker_server
        return self

    def set_input_topic(self, input_topic):
        self.input_topic = input_topic
        return self

    def set_output_topic(self, output_topic):
        self.output_topic = output_topic
        return self

    def set_group_id(self, group_id):
        self.group_id = group_id
        return self

    def set_agg_function(self, agg_function: AggregationFunction):
        self.agg_function = agg_function
        return self

    def set_agg_window_millis(self, agg_window_millis: int):
        self.agg_window_millis = agg_window_millis
        return self

    def build(self) -> BaseStreamBackend:
        if self.agg_function:
            return SparkKafkaStreamBackend(**vars(self).copy())
        else:
            args = vars(self).copy()
            del args["agg_function"]
            del args["agg_window_millis"]
            return KafkaStreamBackend(**args)


class PubSubStreamBuilder(BaseBuilder):

    def __init__(self,
                 project_id: str = None,
                 subscription: str = None,
                 output_topic: str = None,
                 auth_file: str = None,
                 agg_function: AggregationFunction = None,
                 agg_window_millis: int = 0) -> None:
        super().__init__()
        self.project_id = project_id
        self.subscription = subscription
        self.output_topic = output_topic
        self.auth_file = auth_file
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def set_project_id(self, project_id):
        self.project_id = project_id
        return self

    def set_subscription(self, subscription):
        self.subscription = subscription
        return self

    def set_output_topic(self, output_topic):
        self.output_topic = output_topic
        return self

    def set_auth_file(self, auth_file: str):
        self.auth_file = auth_file
        return self

    def build(self) -> BaseStreamBackend:
        if self.agg_function:
            raise NotImplementedError("Not implemented")
        else:
            args = vars(self).copy()
            del args["agg_function"]
            del args["agg_window_millis"]
            return PubSubStreamBackend(**args)


class StreamBuilderFactory(object):

    @staticmethod
    def get_kafka():
        return KafkaStreamBuilder()

    @staticmethod
    def get_pubsub():
        return PubSubStreamBuilder()
