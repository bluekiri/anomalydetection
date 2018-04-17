import json
import argparse
import sqlite3

import sys


def dump(file_path):
    data = json.load(file_path)

    conn = sqlite3.connect('data.db')

    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE predictions
                 (ts text, agg_function text, agg_value real, agg_window_millis integer, ar_value_upper_limit real, ar_anomaly_probability real,ar_value_lower_limit real, ar_is_anomaly real)''')

    for item in data:
        item_data = [item.get]
        c.execute("INSERT INTO predictions VALUES (%s)" % item_data)


# if __name__ == "__main__":
parser = argparse.ArgumentParser(description='Dump json file into a sqlite file.')
parser.add_argument('datain', metavar='din', type=str, help='json_path. Example python from_json_predict_values_to_sqlite ./data.json')
args = parser.parse_args()
dump(args.datain)
