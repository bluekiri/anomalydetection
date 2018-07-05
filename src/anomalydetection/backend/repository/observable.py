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

from rx import Observable

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository import BaseObservableRepository


class ObservableRepository(BaseObservableRepository):

    def __init__(self, repository: BaseRepository,
                 application=None, from_ts=None, to_ts=None) -> None:
        """
        Creates ObservableRepository that is capable to act as an observable

        :param repository:    the repository
        :param application:   application name
        :param from_ts:       from timestamp
        :param to_ts:         to timestamp
        """
        super().__init__(repository)
        self.application = application
        self.from_ts = from_ts
        self.to_ts = to_ts

        if not self.to_ts:
            self.to_ts = datetime.datetime.now()
        if not self.from_ts:
            self.from_ts = self.to_ts - datetime.timedelta(hours=24)

    def _get_observable(self):
        return Observable.from_(self.repository.fetch(self.application,
                                                      self.from_ts,
                                                      self.to_ts))
