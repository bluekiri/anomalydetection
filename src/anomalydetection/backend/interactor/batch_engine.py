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

from anomalydetection.backend.engine.builder import BaseBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import BaseEngineInteractor
from anomalydetection.backend.stream import BaseObservable
from anomalydetection.common.logging import LoggingMixin
from anomalydetection.backend.stream import AggregationFunction


class BatchEngineInteractor(BaseEngineInteractor, LoggingMixin):

    def __init__(self,
                 batch: BaseObservable,
                 engine_builder: BaseBuilder,
                 message_handler: BaseMessageHandler) -> None:
        super().__init__(engine_builder, message_handler)
        self.batch = batch
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
            "agg_function": AggregationFunction.NONE,
            "agg_window_millis": 0,
            "ts": ts,
            "anomaly_results": anomaly_results
        }
        return OutputMessage(**output)

    def process(self) -> list:

        processed = self.batch.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: self.map_with_engine(x))
        return processed.to_blocking()
