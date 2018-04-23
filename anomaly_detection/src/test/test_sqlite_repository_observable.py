import sqlite3
import unittest

from anomalydetection.backend.repository.sqlite import ObservableSQLite


class SQLiteObservableRepository(unittest.TestCase):

    def test(self):
        conn = sqlite3.connect(
            "/home/tofol/Documents/data_signal.sqlite")
        obs_rep = ObservableSQLite(repository=conn)
        obs_rep.get_observable().subscribe(lambda x: print(x))

