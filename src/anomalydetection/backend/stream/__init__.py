# -*- coding:utf-8 -*-

from collections import Generator
from typing import Any

from rx import Observable


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

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")
