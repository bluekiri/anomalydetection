from elasticsearch import Elasticsearch
import json
import pandas as pd

# Define config
host = "clop-elasticsearch-operations.logitravelzone.local"
port = 9200
timeout = 1000
index = "esx-2018.04.03"
doc_type = "type"
size = 1000
body = {}

# Init Elasticsearch instance
es = Elasticsearch(
    [
        {
            'host': host,
            'port': port
        }
    ],
    timeout=timeout
)

total_data = []
global total_data


# Process hits here
def process_hits(hits):
    global total_data
    total_data += [item.get("_source") for item in hits]


# Check index exists
if not es.indices.exists(index=index):
    print("Index " + index + " not exists")
    exit()

# Init scroll by search
data = es.search(
    index=index,
    scroll='2m',
    size=size,
    body=body
)

# Get the scroll ID
sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])

# Before scroll, process current batch of hits
process_hits(data['hits']['hits'])

while scroll_size > 0 and len(total_data):
    "Scrolling..."
    data = es.scroll(scroll_id=sid, scroll='2m')

    # Process current batch of hits
    process_hits(data['hits']['hits'])

    # Update the scroll ID
    sid = data['_scroll_id']

    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])
    print(len(total_data))

df = pd.DataFrame(total_data)
df.to_csv("dump_day_"+index+".tsv", sep="\t")
