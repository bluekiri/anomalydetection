# -*- coding:utf-8 -*- #

import json
import logging

from jsonschema import validate

from anomalydetection.entities.input_message import InputMessage
from anomalydetection.stream import MessageHandler


class InputJsonMessageHandler(MessageHandler[InputMessage]):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

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
        except Exception as e:
            cls.logger.error("Error parsing message", e)
            return None

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        if message:
            return True

