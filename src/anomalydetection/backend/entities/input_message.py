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

import datetime
import json
from typing import Any

import dateutil.parser

from anomalydetection.backend.entities import BaseMessageHandler


class InputMessage:

    def __init__(self,
                 application: str,
                 value: float,
                 ts: Any):
        """
        This is the parser of a json message

        :param application:  application
        :param value:        value
        :param ts:           datetime or current time stamp string in ISO 8601
        """
        if isinstance(ts, str):
            self.ts = dateutil.parser.parse(ts)
        elif isinstance(ts, datetime.datetime):
            self.ts = ts
        self.value = value
        self.application = application

    def to_dict(self):
        return {
            "application": self.application,
            "value": self.value,
            "ts": self.ts
        }

    def to_json(self):
        return json.dumps({
            "application": self.application,
            "value": self.value,
            "ts": str(self.ts)
        })


class InputMessageHandler(BaseMessageHandler[InputMessage]):

    @classmethod
    def parse_message(cls, message: InputMessage) -> InputMessage:
        return message

    @classmethod
    def extract_key(cls, message: InputMessage) -> str:
        return message.application

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        return True
