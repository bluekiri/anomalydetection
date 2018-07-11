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

from typing import Any, List, Iterable

from rx.core import Observable

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.stream import BaseObservable


class BaseRepository(object):

    def __init__(self, conn) -> None:
        super().__init__()
        self.conn = conn

    def initialize(self):
        """
        Initialize the repository
        """
        raise NotImplementedError("To implement in child classes.")

    def fetch(self, application, from_ts, to_ts) -> Iterable:
        """
        Fetch data from repository, should return ordered data

        :param application:    application name
        :param from_ts:        from timestamp
        :param to_ts:          to timestamp
        :return:               an iterable
        """
        raise NotImplementedError("To implement in child classes.")

    def insert(self, message: OutputMessage) -> None:
        """
        Insert an OutputMessage into the repository

        :param message:        an output message
        """
        raise NotImplementedError("To implement in child classes.")

    def map(self, item: Any) -> OutputMessage:
        """
        Map function to map elements returned by fetch method to OutputMessage

        :param item:  an element in fetch iterable
        :return:      an OutputMessage
        """
        raise NotImplementedError("To implement in child classes.")

    def get_applications(self) -> List[str]:
        """
        Return a list of distinct applications contained in the repository.

        :return:    a list of application names
        """
        raise NotImplementedError("To implement in child classes.")


class BaseObservableRepository(BaseObservable):
    """
    Use a repository as an Observable
    """

    def __init__(self, repository: BaseRepository) -> None:
        """
        BaseObservableRepository constructor

        :param repository: a repository
        """
        self.repository = repository

    def _get_observable(self) -> Observable:
        raise NotImplementedError("To implement in child classes.")

    def get_observable(self) -> Observable:
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
