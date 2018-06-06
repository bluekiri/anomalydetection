# -*- coding:utf-8 -*- #
from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.sqlite import SQLiteRepository


class BaseBuilder(object):

    def build(self) -> BaseRepository:
        raise NotImplementedError("To implement on child classes.")


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
    def get_sqlite():
        return SQLiteBuilder()
