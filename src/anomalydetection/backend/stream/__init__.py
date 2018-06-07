# -*- coding:utf-8 -*-

from collections import Generator
from typing import Any

from rx import Observable

from anomalydetection.backend.stream.aggregation_functions import AggregationFunction


class BaseObservable(object):

    def get_observable(self):
        raise NotImplementedError("To implement in child classes.")

    def map(self, x: Any) -> Any:
        return x


class BasePollingStream(BaseObservable):

    def poll(self) -> Generator:
        raise NotImplementedError("To implement in child classes.")

    def get_observable(self):
        return Observable.from_(self.poll())


class BasePushingStream:

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")


class BaseStreamAggregation(object):

    def __init__(self,
                 agg_function: AggregationFunction = None,
                 agg_window_millis: int = None) -> None:
        super().__init__()
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis


class BaseStreamBackend(BasePollingStream, BasePushingStream):

    def __init__(self,
                 poll_stream: BasePollingStream,
                 push_stream: BasePushingStream) -> None:
        super().__init__()
        self.poll_stream = poll_stream
        self.push_stream = push_stream

    def poll(self) -> Generator:
        return self.poll_stream.poll()

    def push(self, message: str) -> None:
        self.push_stream.push(message)
