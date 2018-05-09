# -*- coding:utf-8 -*- #
from datetime import datetime
from typing import TypeVar, Generic, Any

T = TypeVar('T')


class BaseMessageHandler(Generic[T]):

    @classmethod
    def parse_message(cls, message: str) -> T:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_value(cls, message: T) -> Any:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def validate_message(cls, message: T) -> bool:
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_ts(cls, message: T) -> datetime:
        return datetime.now()

    @classmethod
    def extract_extra(cls, message: T) -> dict:
        return {}
