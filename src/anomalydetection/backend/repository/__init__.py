# -*- coding:utf-8 -*- #
from typing import Any

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.stream import BaseObservable


class BaseRepository(object):

    def __init__(self, conn) -> None:
        super().__init__()
        self.conn = conn

    def initialize(self):
        raise NotImplementedError("To implement on child classes.")

    def fetch(self, from_ts, to_ts):
        raise NotImplementedError("To implement on child classes.")

    def insert(self, message: OutputMessage):
        raise NotImplementedError("To implement on child classes.")


class BaseObservableRepository(BaseObservable):

    def _get_observable(self):
        raise NotImplementedError("To implement on child classes.")

    def get_observable(self):
        return self._get_observable().map(lambda x: self.map(x))

    def get_min(self):
        maximum = self.get_observable() \
            .map(lambda x: x.agg_value) \
            .reduce(lambda a, b: a if a < b else b) \
            .to_blocking()
        return [x for x in maximum][0]

    def get_max(self):
        maximum = self.get_observable() \
            .map(lambda x: x.agg_value) \
            .reduce(lambda a, b: a if a > b else b) \
            .to_blocking()
        return [x for x in maximum][0]

    def map(self, item: Any) -> OutputMessage:
        raise NotImplementedError("To implement on child classes.")
