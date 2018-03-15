from kafka import KafkaConsumer


class KafkaRepository:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers


    