from datetime import datetime
from elasticsearch import Elasticsearch

from feed.config import elastic_search_host_endpoint


class ElasticSearchRepository:

    def __init__(self):
        self.es = Elasticsearch(hosts={"host": elastic_search_host_endpoint, "port": 9200})
        pass

    def get_ios_mean(self):
        self.es.search(index="esx-*", body={"query": {"match_all": {}}})
