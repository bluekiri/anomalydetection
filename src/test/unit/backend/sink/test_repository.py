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

import unittest
from datetime import datetime
from typing import List, Any

from rx import Observable

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.sink.repository import \
    RepositorySink
from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.stream import AggregationFunction


class InMemoryRepository(BaseRepository):

    def __init__(self, conn) -> None:
        super().__init__(conn)
        self.storage = {}

    def initialize(self):
        if not self.storage:
            self.storage = {}

    def fetch(self, application, from_ts, to_ts):
        return self.storage[application]

    def insert(self, message: OutputMessage):
        if message.application not in self.storage:
            self.storage[message.application] = []
        self.storage[message.application].append(message)

    def map(self, item: Any) -> OutputMessage:
        return item

    def get_applications(self) -> List[str]:
        return list(self.storage.keys())


class TestRepository(unittest.TestCase):

    RANGE = 10

    def test_subscription(self):
        repository = InMemoryRepository("none")

        def build_output(val):
            return OutputMessage("app", None, 0, AggregationFunction.NONE,
                                 val, datetime.now())

        elements = Observable.from_([build_output(x) for x in range(self.RANGE)])
        elements.subscribe(RepositorySink(repository))

        self.assertListEqual(repository.get_applications(), ["app"])
        self.assertEqual(len(repository.storage["app"]), self.RANGE)
