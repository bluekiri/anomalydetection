# -*- coding:utf-8 -*-

from collections import Generator
from typing import TypeVar, Generic

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


class StreamBackend(object):

    def poll(self) -> Generator:
        raise NotImplementedError("To implement in child classes.")

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")
