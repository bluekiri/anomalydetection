# -*- coding:utf-8 -*-
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

from anomalydetection.backend.stream import BaseStreamProducer
from anomalydetection.backend.sink import Sink
from anomalydetection.common.logging import LoggingMixin


class StreamSink(Sink, LoggingMixin):

    def __init__(self, repository: BaseStreamProducer) -> None:
        super().__init__()
        self.producer = repository

    def on_next(self, value):
        self.producer.push(str(value))

    def on_error(self, error):
        self.logger.error(error)

    def on_completed(self):
        self.logger.debug("{} completed".format(self))
