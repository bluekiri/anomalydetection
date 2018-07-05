# -*- coding:utf-8 -*- #
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

from datetime import datetime
from typing import TypeVar, Generic, Any

T = TypeVar('T')


class BaseMessageHandler(Generic[T]):
    """
    Base message handler
    """

    @classmethod
    def parse_message(cls, message: Any) -> T:
        """
        Parse or transform an input message and returns it

        :param message:  message serialized in a string
        :return:         parsed message
        """
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_key(cls, message: T) -> str:
        """
        Extracts the key of the message, this value is used to group messages

        :param message:  parsed message
        :return:         word
        """
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_value(cls, message: T) -> float:
        """
        Extracts the value of the message, this value is that is given to
        make the prediction

        :param message:  parsed message
        :return:         a float value
        """
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def validate_message(cls, message: T) -> bool:
        """
        Validates a message

        :param message:  validates if a message is valid or not
        :return:         True if is valid, False if is not
        """
        raise NotImplementedError("To implement in child classes.")

    @classmethod
    def extract_ts(cls, message: T) -> datetime:
        """
        Extract the datetime of the message

        :param message:   parsed message
        :return:          a datetime object
        """
        return datetime.now()

    @classmethod
    def extract_extra(cls, message: T) -> dict:
        """
        Extract extra data from the parsed message

        :param message:    parsed message
        :return:           a dict of extra values
        """
        return {}
