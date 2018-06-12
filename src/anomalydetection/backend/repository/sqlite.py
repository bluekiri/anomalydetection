# -*- coding:utf-8 -*- #
import sqlite3
from sqlite3 import Row

from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.entities.output_message import OutputMessage

from anomalydetection.backend.repository import BaseRepository


class SQLiteRepository(BaseRepository):

    def __init__(self, database: str) -> None:
        super().__init__(database)
        self.conn_string = database

    def initialize(self):
        # Check if table exists
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        check = cur.execute("""
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE 1
            AND type='table'
            AND name='predictions'""").fetchone()

        if not check or not check[0]:
            cur.execute("""
                CREATE TABLE predictions (
                    application text,
                    ts text,
                    agg_function text,
                    agg_value real,
                    agg_window_millis integer,
                    ar_value_upper_limit real,
                    ar_anomaly_probability real,
                    ar_value_lower_limit real,
                    ar_is_anomaly real)""")

        self.conn.commit()
        self.conn.close()

    def map(self, item: Row) -> OutputMessage:
        anom_results = AnomalyResult(
            value_lower_limit=item[7],
            value_upper_limit=item[5],
            anomaly_probability=item[6],
            is_anomaly=item[8]
        )
        return OutputMessage(item[0],
                             anom_results,
                             agg_window_millis=item[4],
                             agg_function=item[2],
                             agg_value=item[3],
                             ts=item[1])

    def get_applications(self):
        stmt = """
            SELECT DISTINCT(application)
            FROM predictions
        """
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cursor = cur.execute(stmt)
        elements = cursor.fetchall()
        self.conn.close()
        elements = [x[0] for x in elements]
        return sorted(elements)

    def fetch(self, application, from_ts, to_ts):
        stmt = """
            SELECT
                application,
                ts,
                agg_function,
                agg_value,
                agg_window_millis,
                ar_value_upper_limit,
                ar_anomaly_probability,
                ar_value_lower_limit,
                ar_is_anomaly
            FROM predictions
            WHERE 1
            AND ts BETWEEN ? AND ?
        """
        params = (from_ts, to_ts)
        if application:
            stmt = stmt + """AND application = ?"""
            params = (from_ts, to_ts, application)
        stmt = stmt + """ ORDER BY ts ASC """
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cursor = cur.execute(stmt, params)
        elements = cursor.fetchall()
        self.conn.close()
        return elements

    def insert(self, message: OutputMessage):
        anomaly_results = message.anomaly_results
        anomaly_value = [anomaly_results.value_upper_limit,
                         anomaly_results.anomaly_probability,
                         anomaly_results.value_lower_limit,
                         int(anomaly_results.is_anomaly)]
        root_value = ["'%s'" % message.application,
                      "'%s'" % message.ts,
                      "'%s'" % message.agg_function,
                      message.agg_value,
                      int(message.agg_window_millis)]
        values = ", ".join(map(str, root_value + anomaly_value))
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO predictions VALUES (%s)""" % values)
        self.conn.commit()
        self.conn.close()
