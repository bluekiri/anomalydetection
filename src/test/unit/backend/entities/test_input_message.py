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

import json
import unittest
from datetime import datetime

from anomalydetection.backend.entities.input_message import InputMessage, \
    InputMessageHandler


class TestInputMessage(unittest.TestCase):

    APP = "app"
    VALUE = .8
    NOW = datetime.now()
    NOW_STR = str(NOW)

    def test_constructor(self):

        in_msg_a = InputMessage(self.APP, self.VALUE, self.NOW)
        self.assertEqual(in_msg_a.application, self.APP)
        self.assertEqual(in_msg_a.value, self.VALUE)
        self.assertEqual(in_msg_a.ts, self.NOW)

        in_msg_b = InputMessage(self.APP, self.VALUE, self.NOW_STR)
        self.assertEqual(in_msg_b.application, self.APP)
        self.assertEqual(in_msg_b.value, self.VALUE)
        self.assertEqual(in_msg_b.ts, self.NOW)

    def test_to_dict(self):

        expected = {
            "application": self.APP,
            "value": self.VALUE,
            "ts": self.NOW
        }

        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        self.assertDictEqual(in_msg.to_dict(), expected)

    def test_to_json(self):

        expected = {
            "application": self.APP,
            "value": self.VALUE,
            "ts": self.NOW_STR
        }

        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        self.assertDictEqual(json.loads(in_msg.to_json()), expected)


class TestInputMessageHandler(unittest.TestCase):

    APP = "app"
    VALUE = .8
    NOW = datetime.now()

    def test_parse_message(self):
        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        handler = InputMessageHandler()
        self.assertEqual(handler.parse_message(in_msg), in_msg)

    def test_extract_key(self):
        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        handler = InputMessageHandler()
        self.assertEqual(handler.extract_key(in_msg), in_msg.application)

    def test_extract_value(self):
        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        handler = InputMessageHandler()
        self.assertEqual(handler.extract_value(in_msg), in_msg.value)

    def test_validate_message(self):
        in_msg = InputMessage(self.APP, self.VALUE, self.NOW)
        handler = InputMessageHandler()
        self.assertEqual(handler.validate_message(in_msg), True)
