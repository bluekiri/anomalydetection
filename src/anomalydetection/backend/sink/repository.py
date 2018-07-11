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

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.sink import BaseSink
from anomalydetection.common.logging import LoggingMixin


class RepositorySink(BaseSink, LoggingMixin):

    def __init__(self, repository: BaseRepository) -> None:
        """
        Creates a RepositorySink that is capable to sink OutputMessages into the
        given repository

        :param repository:    a repository
        """
        super().__init__()
        self.repository = repository
        self.repository.initialize()

    def on_next(self, value):
        self.repository.insert(value)

    def on_error(self, error):
        self.logger.error(error)

    def on_completed(self):
        self.logger.debug("{} completed".format(self))
