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

from jsonschema import ValidationError

from anomalydetection.backend.entities.handlers.json import \
    InputJsonMessageHandler


class TestInputJsonMessageHandler(unittest.TestCase):

    VALID_MESSAGE = """
    {
        "application": "app",
        "value": 0.87,
        "ts": "2018-01-01T00:00:00.000"
    }
    """

    INVALID_MESSAGE_1 = """
    {
        "application": "app",
        "ts": "2018-01-01T00:00:00.000"
    }
    """

    INVALID_MESSAGE_2 = """
    {
        "application": "app",
        "value": 0.87
    }
    """

    INVALID_MESSAGE_3 = """
    {
        "value": 0.87,
        "ts": "2018-01-01T00:00:00.000"
    }
    """

    def test_parse_message_and_validate(self):
        handler = InputJsonMessageHandler()
        in_message = handler.parse_message(self.VALID_MESSAGE)
        self.assertEqual(handler.validate_message(in_message), True)

    def test_extract_key(self):
        handler = InputJsonMessageHandler()
        in_message = handler.parse_message(self.VALID_MESSAGE)
        self.assertEqual(handler.extract_key(in_message), "app")

    def test_extract_value(self):
        handler = InputJsonMessageHandler()
        in_message = handler.parse_message(self.VALID_MESSAGE)
        self.assertEqual(handler.extract_value(in_message), 0.87)

    def test_extract_ts(self):
        handler = InputJsonMessageHandler()
        in_message = handler.parse_message(self.VALID_MESSAGE)
        self.assertEqual(handler.extract_ts(in_message), datetime(2018, 1, 1))

    def test_parse_message_and_validate_invalid(self):
        handler = InputJsonMessageHandler()
        with self.assertRaises(ValidationError) as ctx:
            handler.parse_message(self.INVALID_MESSAGE_1)

        self.assertEqual(ctx.exception.message,
                         "'value' is a required property")

        with self.assertRaises(ValidationError) as ctx:
            handler.parse_message(self.INVALID_MESSAGE_2)

        self.assertEqual(ctx.exception.message,
                         "'ts' is a required property")

        with self.assertRaises(ValidationError) as ctx:
            handler.parse_message(self.INVALID_MESSAGE_3)

        self.assertEqual(ctx.exception.message,
                         "'application' is a required property")
