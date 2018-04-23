# -*- coding:utf-8 -*- #
import datetime
from typing import Any

import dateutil.parser


class InputMessage:

    def __init__(self, application: str, value: float, ts: Any):
        """
        This is the parser format of a kafka message.

        :param application: Sender application
        :param value: Value
        :param ts: datetime or current time stamp string in ISO 8601
        """
        if isinstance(ts, str):
            self.ts = dateutil.parser.parse(ts)
        elif isinstance(ts, datetime.datetime):
            self.ts = ts
        self.value = value
        self.application = application
