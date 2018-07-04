# -*- coding: utf-8 -*-
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

from anomalydetection.backend.engine.builder import CADDetectorBuilder

from anomalydetection.common.logging import LoggingMixin
from anomalydetection.dashboard.helpers.engine import EngineBuilderForm


class TestEngineBuilderForm(unittest.TestCase, LoggingMixin):

    def test_get_form(self):
        helper = EngineBuilderForm(CADDetectorBuilder())
        form = helper.get_form()
        self.assertIsInstance(form, list)
