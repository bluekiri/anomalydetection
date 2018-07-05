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

from collections import Generator
from typing import Any

from rx import Observable

from anomalydetection.backend.stream.agg.functions import AggregationFunction


class BaseObservable(object):

    def get_observable(self):
        raise NotImplementedError("To implement in child classes.")

    def map(self, x: Any) -> Any:
        return x


class FileObservable(BaseObservable):

    def __init__(self, file) -> None:
        super().__init__()
        self.file = file

    def get_observable(self):
        return Observable.from_(open(self.file).readlines())


class BaseStreamConsumer(BaseObservable):

    def poll(self) -> Generator:
        raise NotImplementedError("To implement in child classes.")

    def get_observable(self):
        return Observable.from_(self.poll())


class BaseStreamProducer:

    def push(self, message: str) -> None:
        raise NotImplementedError("To implement in child classes.")


class BaseStreamAggregation(object):

    def __init__(self,
                 agg_function: AggregationFunction = None,
                 agg_window_millis: int = None) -> None:
        super().__init__()
        self.agg_function = agg_function
        self.agg_window_millis = agg_window_millis
