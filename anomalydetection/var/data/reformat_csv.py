import pandas as pd
import json
import argparse


def parse_input(default_params):
    parser = argparse.ArgumentParser(description="Reformat csv as json for anomdec PoC")
    parser.add_argument("--file", "-f",
                        help="file to reformat",
                        type=str)
    args = parser.parse_args()
    if args.file:
        default_params['file'] = args.file
    return default_params

params = {'file': 'data.csv'}

if __name__ == '__main__':
    print('Reformating file')
    params = parse_input(params)
    file_path = params['file']
    df = pd.read_csv(file_path)
    df['application'] = 'test1'
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())
    df.rename(columns={'timestamp': 'ts'}, inplace=True)
    json_format = df.T.to_json()
    with open(file_path + '.json', 'w') as f:
        for i in json.loads(json_format):
            f.write(str(json.loads(json_format)[i])+'\n')
    print('Done')
