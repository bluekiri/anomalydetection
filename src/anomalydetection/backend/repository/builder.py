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
import importlib

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.sqlite import SQLiteRepository


class BaseRepositoryBuilder(object):
    """
    BaseBuilder, implement this to create Repository Builders.
    """

    def build(self) -> BaseRepository:
        """
        Build a repository

        :return: A BaseRepository implementation instance.
        """
        raise NotImplementedError("To implement in child classes.")

    def set(self, name: str, value: str):
        def raise_exception(*args, **kwargs):
            raise NotImplementedError()
        func_name = "set_{}".format(name)
        func = getattr(self, func_name, raise_exception)
        try:
            return func(value)
        except NotImplementedError as ex:
            raise NotImplementedError(
                "Calling undefined function: {}.{}()".format(
                    self.__class__.__name__, func_name))


class SQLiteBuilder(BaseRepositoryBuilder):

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
    def get_plugin(name) -> BaseRepositoryBuilder:
        module_name = "anomalydetection.backend.repository.{}_builder".format(name)
        objects = vars(importlib.import_module(module_name))["_objects"]
        for obj in objects:
            if issubclass(obj, BaseRepositoryBuilder):
                return obj()
        raise NotImplementedError()

    @staticmethod
    def get(name) -> BaseRepositoryBuilder:
        def raise_exception():
            raise NotImplementedError()
        func_name = "get_{}".format(name)
        func = getattr(RepositoryBuilderFactory, func_name, raise_exception)
        try:
            return func()
        except NotImplementedError as ex:
            try:
                return RepositoryBuilderFactory.get_plugin(name)
            except NotImplementedError as ex:
                raise NotImplementedError(
                    "Calling undefined function: {}.{}()".format(
                        "RepositoryBuilderFactory", func_name))

    @staticmethod
    def get_sqlite() -> SQLiteBuilder:
        return SQLiteBuilder()
