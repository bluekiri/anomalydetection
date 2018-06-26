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
from unittest.mock import patch
from datetime import datetime

from rx import Observable

from anomalydetection.backend.entities.output_message import OutputMessage
from anomalydetection.backend.repository import BaseRepository, BaseObservableRepository
from anomalydetection.backend.stream import AggregationFunction


class TestBaseRepository(unittest.TestCase):

    CONN = "none"
    APP = "app"
    FROM = datetime(2018, 1, 1)
    TO = datetime(2018, 1, 2)

    def test_constructor(self):
        repository = BaseRepository(self.CONN)
        self.assertEqual(repository.conn, self.CONN)

    def test_initialize(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            repository.initialize()

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")

    def test_fetch(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            repository.fetch(self.APP, self.FROM, self.TO)

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")

    def test_insert(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            repository.insert(OutputMessage(self.APP, None, 0,
                                            AggregationFunction.NONE, 0,
                                            self.FROM))

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")

    def test_map(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            repository.map(None)

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")

    def test_get_applications(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            repository.get_applications()

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")


class TestBaseObservableRepository(unittest.TestCase):

    CONN = "none"
    VALUES = [1, 2, 3, 4, 5, 6]

    def test_constructor(self):
        repository = BaseRepository(self.CONN)
        observable_repo = BaseObservableRepository(repository)
        self.assertEqual(repository.conn, observable_repo.repository.conn)

    @patch('anomalydetection.backend.repository.BaseObservableRepository._get_observable')
    @patch('anomalydetection.backend.repository.BaseRepository.map')
    def test_get_min(self, map_method, _get_observable_method):

        def mocked__get_observable_method(*args, **kwargs):
            return Observable.from_(self.VALUES)

        _get_observable_method.side_effect = mocked__get_observable_method

        def mocked_map_method(*args, **kwargs):
            return OutputMessage("app", None, 0, AggregationFunction.NONE,
                                 args[0], datetime.now())

        map_method.side_effect = mocked_map_method

        repository = BaseRepository(self.CONN)
        observable_repo = BaseObservableRepository(repository)
        self.assertEqual(observable_repo.get_min(), 1)

    @patch('anomalydetection.backend.repository.BaseObservableRepository._get_observable')
    @patch('anomalydetection.backend.repository.BaseRepository.map')
    def test_get_max(self, map_method, _get_observable_method):

        def mocked__get_observable_method(*args, **kwargs):
            return Observable.from_(self.VALUES)

        _get_observable_method.side_effect = mocked__get_observable_method

        def mocked_map_method(*args, **kwargs):
            return OutputMessage("app", None, 0, AggregationFunction.NONE,
                                 args[0], datetime.now())

        map_method.side_effect = mocked_map_method

        repository = BaseRepository(self.CONN)
        observable_repo = BaseObservableRepository(repository)
        self.assertEqual(observable_repo.get_max(), 6)

    @patch('anomalydetection.backend.repository.BaseObservableRepository._get_observable')
    def test_get_observable(self, _get_observable_method):

        def mocked__get_observable_method(*args, **kwargs):
            return Observable.from_(self.VALUES)

        _get_observable_method.side_effect = mocked__get_observable_method

        repository = BaseRepository(self.CONN)
        observable_repo = BaseObservableRepository(repository)
        self.assertIsInstance(observable_repo.get_observable(), Observable)

    def test__get_observable(self):

        with self.assertRaises(NotImplementedError) as ctx:
            repository = BaseRepository(self.CONN)
            observable_repo = BaseObservableRepository(repository)
            observable_repo._get_observable()

        self.assertEqual(ctx.exception.args[0],
                         "To implement in child classes.")
