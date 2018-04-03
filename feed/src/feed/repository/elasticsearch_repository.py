import datetime
from elasticsearch import Elasticsearch

from feed.conf.config import elastic_search_host_endpoint


class ElasticSearchRepository:

    def __init__(self):
        self.es = Elasticsearch(hosts=[{"host": elastic_search_host_endpoint, "port": 9200}])

    def get_total_write_and_reads(self):
        date = datetime.datetime.utcnow().strftime("%Y.%m.%d")
        gte_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        search = self.es.search(index="esx-%s" % date, body={"query": {
            "range": {"timestamp": {"gte": gte_time.isoformat(), "lte": "now"}}},
            "aggs": {
                "total_writes": {"sum": {"field": "IOWrite"}},
                "total_read": {"sum": {"field": "IORead"}}}
        })
        aggregations = search.get("aggregations")
        return aggregations.get("total_read").get("value"), aggregations.get("total_writes").get("value")
