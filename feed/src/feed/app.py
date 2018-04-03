import time
from datetime import datetime

from feed.conf.config import bootstrap_server, broker_server, read_feed_topic, write_feed_topic
from feed.repository.elasticsearch_repository import ElasticSearchRepository
import schedule

from feed.repository.kafka_repository import KafkaRepository


def main():
    elastic_search_repository = ElasticSearchRepository()
    kafka_repository = KafkaRepository(bootstrap_servers=bootstrap_server, broker_list=broker_server)

    def emit_writes_and_reads():
        total_read, total_writes = elastic_search_repository.get_total_write_and_reads()
        kafka_repository.emit_message(topic=read_feed_topic,
                                      message={"application": "total_read", "value": total_read,
                                               "ts": datetime.utcnow().isoformat()})
        kafka_repository.emit_message(topic=write_feed_topic,
                                      message={"application": "total_writes", "value": total_writes,
                                               "ts": datetime.utcnow().isoformat()})

    schedule.every(5).minutes.do(emit_writes_and_reads)
    for item in range(40):
        emit_writes_and_reads()
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    time.sleep(15)
    main()
