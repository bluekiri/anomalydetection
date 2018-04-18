# -*- coding:utf-8 -*-

from collections import Generator
from datetime import datetime
from typing import TypeVar, Generic

from rx import Observer

T = TypeVar('T')


class MessageHandler(Generic[T]):

    @classmethod
    def parse_message(cls, message: str) -> T:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_value(cls, message: T) -> float:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def validate_message(cls, message: T) -> bool:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_ts(cls, message: T) -> datetime:
        return datetime.now()



class StreamBase(object):

    def poll(self) -> Generator:
        raise NotImplementedError("To implement in child classes.")


class BatchBase(StreamBase):
    pass


class StreamBackend(StreamBase):

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")
