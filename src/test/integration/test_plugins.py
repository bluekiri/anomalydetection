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

from anomalydetection.common import plugins  # noqa: F401
from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.entities.handlers.factory import MessageHandlerFactory
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.stream.builder import StreamBuilderFactory
from anomalydetection.common.logging import LoggingMixin


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    @unittest.skip("FIXME")
    def test_modules(self):
        EngineBuilderFactory.get("plugin1").build()
        RepositoryBuilderFactory.get("plugin1").build()
        StreamBuilderFactory.get_consumer("plugin1").build()
        StreamBuilderFactory.get_producer("plugin1").build()
        MessageHandlerFactory.get("plugin1")
