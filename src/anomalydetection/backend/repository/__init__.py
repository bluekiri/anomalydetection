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

from typing import Any, List

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.stream import BaseObservable


class BaseRepository(object):

    def __init__(self, conn) -> None:
        super().__init__()
        self.conn = conn

    def initialize(self):
        raise NotImplementedError("To implement on child classes.")

    def fetch(self, application, from_ts, to_ts):
        raise NotImplementedError("To implement on child classes.")

    def insert(self, message: OutputMessage):
        raise NotImplementedError("To implement on child classes.")

    def map(self, item: Any) -> OutputMessage:
        raise NotImplementedError("To implement on child classes.")

    def get_applications(self) -> List[str]:
        raise NotImplementedError("To implement on child classes.")


class BaseObservableRepository(BaseObservable):

    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    def _get_observable(self):
        raise NotImplementedError("To implement on child classes.")

    def get_observable(self):
        return self._get_observable().map(lambda x: self.repository.map(x))

    def get_min(self):
        maximum = self.get_observable() \
            .map(lambda x: x.agg_value) \
            .reduce(lambda a, b: a if a < b else b) \
            .to_blocking()
        return [x for x in maximum][0]

    def get_max(self):
        maximum = self.get_observable() \
            .map(lambda x: x.agg_value) \
            .reduce(lambda a, b: a if a > b else b) \
            .to_blocking()
        return [x for x in maximum][0]
