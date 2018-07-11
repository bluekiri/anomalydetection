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

import json
from datetime import datetime

from jsonschema import validate
from jsonschema.exceptions import _Error as JsonSchemaError

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities import BaseMessageHandler


class InputJsonMessageHandler(BaseMessageHandler[InputMessage]):

    JSON_SCHEMA = {
        "$id": "anomaly-detection",
        "type": "object",
        "properties": {
            "application": {
                "$id": "/properties/application",
                "type": "string"
            },
            "ts": {
                "$id": "/properties/ts",
                "type": "string"
            },
            "value": {
                "$id": "/properties/value",
                "type": "number"
            }
        },
        "required": [
            "application",
            "ts",
            "value"
        ]
    }

    @classmethod
    def parse_message(cls, message: str) -> InputMessage:
        data = json.loads(message)
        try:
            validate(data, cls.JSON_SCHEMA)
            return InputMessage(data["application"],
                                data["value"],
                                data["ts"])
        except JsonSchemaError as ex:
            raise ex

    @classmethod
    def extract_key(cls, message: InputMessage) -> str:
        return message.application

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        if message:
            return True
        return False

    @classmethod
    def extract_ts(cls, message: InputMessage) -> datetime:
        return message.ts

    @classmethod
    def extract_extra(cls, message: InputMessage) -> dict:
        return {"ts": message.ts}
