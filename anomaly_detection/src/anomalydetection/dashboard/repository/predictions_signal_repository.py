import sqlite3

from anomalydetection.dashboard.repository.sqlite import get_sql_connection


class PredictionSignalRepository:
    def __init__(self):
        self.db = get_sql_connection()

    def get_application_signal(self, application: str):
        return self.db.session.execute(
            "SELECT application, "
            "ts, "
            "agg_function, "
            "agg_value, "
            "agg_window_millis, "
            "ar_value_upper_limit, "
            "ar_anomaly_probability,"
            "ar_value_lower_limit, "
            "ar_is_anomaly FROM predictions").fetchall()
