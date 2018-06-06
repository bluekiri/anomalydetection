# -*- coding:utf-8 -*- #

import unittest
from datetime import datetime

from anomalydetection.backend.entities.output_message import OutputMessage, \
    AnomalyResult
from anomalydetection.backend.repository.observable import ObservableRepository
from anomalydetection.backend.repository.sqlite import SQLiteRepository
from test import config, LoggingMixin


class SQLiteObservableRepository(unittest.TestCase, LoggingMixin):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.repo = SQLiteRepository(config["SQLITE_DATABASE_FILE"])
        self.repo.initialize()
        anom = AnomalyResult(-1, 1, 0.5, False)
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       1, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       4, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       3, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       2, ts=datetime.now()))

    def test_observable_sqlite(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        obs_rep.get_observable() \
            .subscribe(lambda x: self.logger.debug(str(x)))

    def test_get_min(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        self.assertEqual(1, obs_rep.get_min())

    def test_get_max(self):
        obs_rep = ObservableRepository(self.repo, application="app")
        self.assertEqual(4, obs_rep.get_max())
