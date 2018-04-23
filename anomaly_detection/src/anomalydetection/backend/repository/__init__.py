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


class BaseObservableRepository(BaseRepository, BaseObservable):

    def map(self, item: Any) -> OutputMessage:
        raise NotImplementedError("To implement on child classes.")
