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

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.sqlite import SQLiteRepository


class BaseBuilder(object):
    """
    BaseBuilder, implement this to create Repository Builders.
    """

    def build(self) -> BaseRepository:
        """
        Build a repository

        :return: A BaseRepository implementation instance.
        """
        raise NotImplementedError("To implement in child classes.")


class SQLiteBuilder(BaseBuilder):

    def __init__(self,
                 database: str = None) -> None:
        super().__init__()
        self.database = database

    def set_database(self, database):
        self.database = database
        return self

    def build(self) -> BaseRepository:
        return SQLiteRepository(**vars(self).copy())


class RepositoryBuilderFactory(object):

    @staticmethod
    def get_sqlite() -> SQLiteBuilder:
        return SQLiteBuilder()
