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
from unittest.mock import patch

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository.observable import ObservableRepository


class TestObservableRepository(unittest.TestCase):

    APP = "app"
    FROM = datetime(2018, 1, 1)
    TO = datetime(2018, 1, 10)
    VALUES = [1, 2, 3, 4, 5, 6]

    def test_constructor(self):

        observable_repository = ObservableRepository(
            BaseRepository(None),
            self.APP,
            self.FROM,
            self.TO)
        self.assertIsInstance(observable_repository.repository, BaseRepository)
        self.assertEqual(observable_repository.application, self.APP)
        self.assertEqual(observable_repository.from_ts, self.FROM)
        self.assertEqual(observable_repository.to_ts, self.TO)

    @patch('anomalydetection.backend.repository.BaseRepository.fetch')
    def test__get_observable(self, fetch_method):

        def mocked_fetch_method(*args, **kwargs):
            return self.VALUES

        fetch_method.side_effect = mocked_fetch_method

        observable_repository = ObservableRepository(
            BaseRepository(None),
            self.APP,
            self.FROM,
            self.TO)

        obs = [x for x in observable_repository._get_observable().to_blocking()]
        self.assertListEqual(obs, self.VALUES)
