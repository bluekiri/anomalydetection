import os
import unittest

from anomalydetection.backend.repository.sqlite import ObservableSQLite, \
    SQLiteRepository


class SQLiteObservableRepository(unittest.TestCase):

    def test(self):
        obs_rep = ObservableSQLite(SQLiteRepository(os.environ["DATA_DB_FILE"]))
        obs_rep.get_observable().subscribe(lambda x: print(x))

