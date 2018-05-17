# -*- coding:utf-8 -*- #
import datetime
import sqlite3
from sqlite3 import Row

from rx import Observable

from anomalydetection.backend.entities.output_message import OutputMessage, \
    AnomalyResult
from anomalydetection.backend.repository import \
    BaseObservableRepository, BaseRepository


class SQLiteRepository(BaseRepository):

    def __init__(self, conn_string: str) -> None:
        super().__init__(conn_string)
        self.conn_string = conn_string

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

    def fetch(self, from_ts, to_ts):
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
            WHERE ts BETWEEN ? AND ?
        """
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cursor = cur.execute(stmt, (from_ts, to_ts))
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
                      message.agg_window_millis]
        values = ", ".join(map(str, root_value + anomaly_value))
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO predictions VALUES (%s)""" % values)
        self.conn.commit()
        self.conn.close()


class ObservableSQLite(BaseObservableRepository):

    def __init__(self, repository: BaseRepository,
                 from_ts=None, to_ts=None) -> None:
        self.repository = repository
        self.from_ts = from_ts
        self.to_ts = to_ts

        if not self.to_ts:
            self.to_ts = datetime.datetime.now()
        if not self.from_ts:
            self.from_ts = self.to_ts - datetime.timedelta(hours=24)

    def _get_observable(self):
        return Observable.from_(self.repository.fetch(self.from_ts,
                                                      self.to_ts))

    def map(self, row: Row) -> OutputMessage:
        anom_results = AnomalyResult(
            value_lower_limit=row[7],
            value_upper_limit=row[5],
            anomaly_probability=row[6],
            is_anomaly=row[8]
        )
        return OutputMessage(row[0],
                             anom_results,
                             agg_window_millis=row[4],
                             agg_function=row[2],
                             agg_value=row[3],
                             ts=row[1])
