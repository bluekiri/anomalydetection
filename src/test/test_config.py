# -*- coding:utf-8 -*- #
import unittest

from anomalydetection.common.config import Config
from test import LoggingMixin


class TestConfig(unittest.TestCase, LoggingMixin):

    def setUp(self):
        super().setUp()
        self.config = Config("devel")

    def test_get_signals(self):
        print(self.config)

    def test_get_middlewares(self):
        print(self.config)

    def test_get_warmups(self):
        print(self.config)
