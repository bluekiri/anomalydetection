import json
import argparse
import sqlite3

import os


def dump(file_path):
    data = []

    with open(file_path) as b:
        for line in b.readlines():
            data.append(json.loads(line))

    file_db = "/tmp/data.db"

    if os.path.isfile(file_db):
        os.remove(file_db)
    conn = sqlite3.connect(file_db)

    c = conn.cursor()

    if not len(list(conn.execute("SELECT name FROM sqlite_master WHERE type='table';"))):
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

    def format_inset_data(item_to_format):
        anomaly_results = item_to_format.get("anomaly_results")
        anomaly_value = [anomaly_results.get("value_upper_limit"), anomaly_results.get("anomaly_probability"),
                         anomaly_results.get("value_lower_limit"), anomaly_results.get("is_anomaly")]
        root_value = ["'%s'" % item_to_format.get("application"), "'%s'" % item_to_format.get("ts"),
                      "'%s'" % item_to_format.get("agg_function"), item_to_format.get("agg_value"),
                      item_to_format.get("agg_window_millis")]
        return ",".join(map(str, root_value + anomaly_value))

    for item in data:
        c.execute("INSERT INTO predictions VALUES (%s)" % format_inset_data(item))

    conn.commit()
    conn.close()


# if __name__ == "__main__":
parser = argparse.ArgumentParser(description='Dump json file into a sqlite file.')
parser.add_argument('datain', metavar='din', type=str,
                    help='json_path. Example python from_json_predict_values_to_sqlite ./data.json')
args = parser.parse_args()
dump(args.datain)
