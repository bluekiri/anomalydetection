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

import os
import unittest

from anomalydetection.backend.engine.builder import EngineBuilderFactory
from anomalydetection.backend.entities.handlers.factory import MessageHandlerFactory
from anomalydetection.backend.repository.builder import RepositoryBuilderFactory
from anomalydetection.backend.stream.builder import StreamBuilderFactory
from anomalydetection.common.logging import LoggingMixin
from test import TEST_PATH


class TestPubSubStreamBackend(unittest.TestCase, LoggingMixin):

    PLUGIN_NAME = "test"

    def test_modules(self):

        os.environ["ANOMDEC_HOME"] = TEST_PATH + "/anomdec_home_test"

        from anomalydetection.backend.core import plugins  # noqa: F401
        EngineBuilderFactory.get(self.PLUGIN_NAME).build()
        RepositoryBuilderFactory.get(self.PLUGIN_NAME).build()
        StreamBuilderFactory.get_consumer(self.PLUGIN_NAME).build()
        StreamBuilderFactory.get_producer(self.PLUGIN_NAME).build()
        MessageHandlerFactory.get(self.PLUGIN_NAME)

        del os.environ["ANOMDEC_HOME"]
