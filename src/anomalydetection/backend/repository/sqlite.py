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

import datetime
import sqlite3
from sqlite3 import Row
from typing import Iterable

from anomalydetection.backend.entities.output_message import AnomalyResult
from anomalydetection.backend.entities.output_message import OutputMessage

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.stream import AggregationFunction


class SQLiteRepository(BaseRepository):

    def __init__(self, database: str) -> None:
        """
        SQLiteRepository constructor

        :param database:  database path
        """
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
        fmt = "%Y-%m-%d %H:%M:%S"
        return OutputMessage(item[0],
                             anom_results,
                             agg_window_millis=item[4],
                             agg_function=AggregationFunction(item[2]),
                             agg_value=item[3],
                             ts=datetime.datetime.strptime(item[1][0:19], fmt))

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

    def fetch(self, application, from_ts, to_ts) -> Iterable[Row]:
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
                      "'%s'" % message.agg_function.value,
                      message.agg_value,
                      int(message.agg_window_millis)]
        values = ", ".join(map(str, root_value + anomaly_value))
        self.conn = sqlite3.connect(self.conn_string)
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO predictions VALUES (%s)""" % values)
        self.conn.commit()
        self.conn.close()
