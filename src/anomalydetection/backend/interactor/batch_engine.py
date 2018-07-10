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

from rx.core import Observable

from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.interactor import BaseEngineInteractor
from anomalydetection.backend.stream import BaseObservable
from anomalydetection.common.logging import LoggingMixin
from anomalydetection.backend.stream import AggregationFunction


class BatchEngineInteractor(BaseEngineInteractor, LoggingMixin):

    """
    BatchEngineInteractor is an implementation for batch process
    an Observable
    """

    def __init__(self,
                 batch: BaseObservable,
                 engine_builder: BaseEngineBuilder,
                 message_handler: BaseMessageHandler) -> None:
        """
        BatchEngineInteractor constructor

        :param batch:             an observable
        :param engine_builder:    an engine builder
        :param message_handler:   a message handler
        """
        super().__init__(engine_builder, message_handler)
        self.batch = batch

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

    def process(self) -> Observable:
        processed = self.batch.get_observable() \
            .map(lambda x: self.message_handler.parse_message(x)) \
            .filter(lambda x: self.message_handler.validate_message(x)) \
            .map(lambda x: self.map_with_engine(x))
        return processed.to_blocking()
