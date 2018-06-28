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

from anomalydetection.backend.repository.builder import BaseBuilder
from anomalydetection.backend.repository.builder import SQLiteBuilder
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.repository.sqlite import SQLiteRepository


class TestBaseBuilder(unittest.TestCase):

    def test_build(self):
        with self.assertRaises(NotImplementedError) as ctx:
            builder = BaseBuilder()
            builder.build()

        self.assertEqual(str(ctx.exception), "To implement in child classes.")


class TestSQLiteBuilder(unittest.TestCase):

    DB_FILE = "/dev/null"

    def test_constructor(self):
        builder = SQLiteBuilder()
        builder.set_database(self.DB_FILE)
        self.assertEqual(builder.database, self.DB_FILE)

    def test_build(self):
        builder = SQLiteBuilder()
        builder.set_database(self.DB_FILE)
        self.assertIsInstance(builder.build(), SQLiteRepository)


class TestRepositoryBuilderFactory(unittest.TestCase):

    def test_get_sqlite(self):
        builder = RepositoryBuilderFactory.get_sqlite()
        self.assertIsInstance(builder, SQLiteBuilder)
