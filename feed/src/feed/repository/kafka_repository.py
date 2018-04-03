from kafka import KafkaProducer
import json



class KafkaRepository:

    def __init__(self, bootstrap_servers, broker_list):
        self.broker_list = broker_list
        self.bootstrap_servers = bootstrap_servers
        print("Connect to %s" % bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=self.broker_list, api_version=(0, 10))

    def emit_message(self, topic, message):
        message = json.dumps(message)
        self.producer.send(topic, bytearray(message, 'utf8'))
