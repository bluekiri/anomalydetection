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

from typing import List

from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import BaseEngineInteractor
from anomalydetection.backend.sink import BaseSink
from anomalydetection.backend.stream import BaseStreamAggregation
from anomalydetection.backend.stream import AggregationFunction
from anomalydetection.backend.stream import BaseObservable
from anomalydetection.backend.stream.builder import BaseConsumerBuilder
from anomalydetection.common.logging import LoggingMixin


class StreamEngineInteractor(BaseEngineInteractor, LoggingMixin):

    def __init__(self,
                 stream: BaseConsumerBuilder,
                 engine_builder: BaseEngineBuilder,
                 message_handler: BaseMessageHandler,
                 sinks: List[BaseSink] = list(),
                 warm_up: BaseObservable = None) -> None:
        super().__init__(engine_builder, message_handler)
        self.stream = stream.build()
        self.sinks = sinks
        self.warm_up = warm_up
        if isinstance(self.stream, BaseStreamAggregation):
            self.agg_function = self.stream.agg_function
            self.agg_window_millis = self.stream.agg_window_millis
        else:
            self.agg_function = AggregationFunction.NONE
            self.agg_window_millis = 0
        self.app_engine = {}

    def map_with_engine(self, input_message: InputMessage) -> OutputMessage:
        key = self.message_handler.extract_key(input_message)
        value = self.message_handler.extract_value(input_message)
        extra_values = self.message_handler.extract_extra(input_message)

        anomaly_results = \
            self.get_engine(key) \
                .predict(value, **extra_values)

        ts = self.message_handler.extract_ts(input_message)
        output = {
            "application": key,
            "agg_value": value,
            "agg_function": self.agg_function,
            "agg_window_millis": self.agg_window_millis,
            "ts": ts,
            "anomaly_results": anomaly_results
        }
        return OutputMessage(**output)

    def run(self):

        if self.warm_up:
            warm_up = self.warm_up.get_observable() \
                .map(lambda x: self.map_with_engine((x.to_input()))) \
                .to_blocking()
            len([x for x in warm_up])  # Force model to consume messages
            self.logger.info("Warm up completed.")

        # Parse input
        stream = self.stream.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \

        # Aggregate and map input values.
        rx = stream \
            .filter(lambda x: x) \
            .map(lambda x: self.map_with_engine(x)) \
            .publish()  # This is required for multiple subscriptions

        # Sinks
        for sink in self.sinks:
            rx.subscribe(sink)

        # Connect with observers
        rx.connect()

        return rx
