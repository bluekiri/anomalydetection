# -*- coding:utf-8 -*-
from anomalydetection.backend.conf.config import SQLITE_DATABASE_FILE
from anomalydetection.backend.store_middleware import Middleware
import sqlite3


class SqliteStoreMiddleware(Middleware):

    def __init__(self, logger) -> None:
        super().__init__()
        self.logger = logger

        self._check_table_exists()

    @classmethod
    def _get_sqlite_connection(self):
        return sqlite3.connect(SQLITE_DATABASE_FILE)

    @classmethod
    def _check_table_exists(self):
        conn = self._get_sqlite_connection()
        c = conn.cursor()
        if not len(list(conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"))):
            # Create table
            c.execute('''CREATE TABLE predictions (
            application text, 
            ts text, 
            agg_function text, 
            agg_value real, 
            agg_window_millis integer, 
            ar_value_upper_limit real, 
            ar_anomaly_probability real,
            ar_value_lower_limit real, 
            ar_is_anomaly real
            )''')

        conn.commit()
        conn.close()

    @classmethod
    def format_inset_data(self, item_to_format):
        anomaly_results = item_to_format.anomaly_results
        anomaly_value = [anomaly_results.value_upper_limit,
                         anomaly_results.anomaly_probability,
                         anomaly_results.value_lower_limit,
                         anomaly_results.is_anomaly]
        root_value = ["'%s'" % item_to_format.application,
                      "'%s'" % item_to_format.ts,
                      "'%s'" % item_to_format.agg_function,
                      item_to_format.agg_value,
                      item_to_format.agg_window_millis]
        return ",".join(map(str, root_value + anomaly_value))

    def on_next(self, value):
        conn = self._get_sqlite_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions VALUES (%s)" % self.format_inset_data(
                value))
        conn.commit()
        conn.close()

    def on_error(self, error):
        self.logger.error(error)

    def on_completed(self):
        self.logger.info("Completed!")
