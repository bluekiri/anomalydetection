import os

bootstrap_server = os.environ["BOOTSTRAP_SERVER"].split(',')
broker_server = os.environ["BROKER_SERVER"].split(',')

write_feed_topic = os.environ["WRITE_FEED_TOPIC"]
read_feed_topic = os.environ["READ_FEED_TOPIC"]

default_period_time = os.environ["PERIOD_IN_SECONDS"]

# Elasticsearch
elastic_search_host_endpoint = "clop-elasticsearch-operations.logitravelzone.local"
