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


class BaseStreamBackend(BasePollingStream):

    def __init__(self,
                 agg_function: AggregationFunction = None,
                 agg_window_millis: int = None) -> None:
        super().__init__()
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")
