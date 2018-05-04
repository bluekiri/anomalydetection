# -*- coding:utf-8 -*- #

import os
import unittest
from datetime import datetime

from anomalydetection.backend.entities.output_message import OutputMessage, AnomalyResult
from anomalydetection.backend.repository.sqlite import ObservableSQLite, \
    SQLiteRepository
from test import config, LoggingMixin


class SQLiteObservableRepository(unittest.TestCase, LoggingMixin):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.repo = SQLiteRepository(config["DATA_DB_FILE"])
        self.repo.initialize()
        anom = AnomalyResult(-1, 1, 0.5, False)
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       1, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       1, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       1, ts=datetime.now()))
        self.repo.insert(OutputMessage("app", anom, 1, "none",
                                       1, ts=datetime.now()))

    def test(self):
        obs_rep = ObservableSQLite(self.repo)
        obs_rep.get_observable() \
            .subscribe(lambda x: self.logger.debug(str(x)))

