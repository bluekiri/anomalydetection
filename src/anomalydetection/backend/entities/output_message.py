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

from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream import AggregationFunction


class AnomalyResult(object):

    """
    AnomalyResult description

    :cvar value_lower_limit:     lower bound limit
    :cvar value_upper_limit:     upper bound limit
    :cvar anomaly_probability:   probability of being anomalous
    :cvar is_anomaly:            if its anomalous or not
    """

    def __init__(self,
                 value_lower_limit: float,
                 value_upper_limit: float,
                 anomaly_probability: float,
                 is_anomaly: bool) -> None:
        """
        AnomalyResults constructor

        :param value_lower_limit:     lower bound limit
        :param value_upper_limit:     upper bound limit
        :param anomaly_probability:   probability of being anomalous
        :param is_anomaly:            if its anomalous or not
        """
        super().__init__()
        self.value_lower_limit = value_lower_limit
        self.value_upper_limit = value_upper_limit
        self.anomaly_probability = anomaly_probability
        self.is_anomaly = is_anomaly

    def to_dict(self):
        return dict(value_lower_limit=self.value_lower_limit,
                    value_upper_limit=self.value_upper_limit,
                    anomaly_probability=self.anomaly_probability,
                    is_anomaly=self.is_anomaly)

    def __dict__(self):
        return self.to_dict()

    def __eq__(self, o: object) -> bool:
        if super().__eq__(o):
            return True
        else:
            if not isinstance(o, type(self)):
                return False
            else:
                return self.value_lower_limit == o.value_lower_limit \
                    and self.value_upper_limit == o.value_upper_limit \
                    and self.anomaly_probability == o.anomaly_probability \
                    and self.is_anomaly == o.is_anomaly


class OutputMessage(object):

    """
    OutputMessage class description

    :cvar application:        application name
    :cvar anomaly_results:    anomaly results
    :cvar agg_window_millis:  aggregation window in milliseconds
    :cvar agg_function:       aggregation function
    :cvar agg_value:          the value after aggregation
    :cvar ts:                 timestamp
    """

    def __init__(self,
                 application: str,
                 anomaly_results: AnomalyResult,
                 agg_window_millis: int = 0,
                 agg_function: AggregationFunction = AggregationFunction.NONE,
                 agg_value: float = 0,
                 ts: datetime = datetime.datetime.now()):
        """
        OutputMessage class constructor

        :param application:        application name
        :param anomaly_results:    anomaly results
        :param agg_window_millis:  aggregation window in milliseconds
        :param agg_function:       aggregation function
        :param agg_value:          the value after aggregation
        :param ts:                 timestamp
        """
        self.application = application
        self.anomaly_results = anomaly_results
        self.agg_window_millis = agg_window_millis
        self.agg_function = agg_function
        self.agg_value = agg_value
        self.ts = ts

    def to_dict(self, ts2str=False):
        return dict(application=self.application,
                    anomaly_results=self.anomaly_results.to_dict(),
                    agg_window_millis=self.agg_window_millis,
                    agg_function=self.agg_function.value,
                    agg_value=self.agg_value,
                    ts=self.ts if not ts2str else str(self.ts))

    def to_plain_dict(self):
        me = self.to_dict(True)
        me.update(**me['anomaly_results'].copy())
        del me['anomaly_results']
        return me

    def to_input(self):
        return InputMessage(self.application, self.agg_value, self.ts)

    def __str__(self):
        response = self.to_dict(True)
        return json.dumps(response)


class OutputMessageHandler(BaseMessageHandler[InputMessage]):

    @classmethod
    def parse_message(cls, message: OutputMessage) -> InputMessage:
        return message.to_input()

    @classmethod
    def extract_key(cls, message: InputMessage) -> str:
        return message.application

    @classmethod
    def extract_value(cls, message: InputMessage) -> float:
        return message.value

    @classmethod
    def validate_message(cls, message: InputMessage) -> bool:
        return True

    @classmethod
    def extract_extra(cls, message: InputMessage) -> dict:
        return {"ts": message.ts}
