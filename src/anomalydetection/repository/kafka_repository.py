from kafka import KafkaConsumer
from kafka import KafkaProducer
from jsonschema import validate
import json

from src.anomalydetection.entities.input_message import InputMessage


class KafkaRepository:
    kafka_input_json_schema = {
        "$id": "anomaly-detection",
        "type": "object",
        "properties": {
            "application": {
                "$id": "/properties/application",
                "type": "string"
            },
            "ts": {
                "$id": "/properties/ts",
                "type": "string"
            },
            "value": {
                "$id": "/properties/value",
                "type": "number"
            }
        },
        "required": [
            "application",
            "ts",
            "value"
        ]
    }

    def __init__(self, bootstrap_servers, broker_list):
        self.broker_list = broker_list
        self.bootstrap_servers = bootstrap_servers
        print("Connect to %s" % bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=self.broker_list, api_version=(0, 10))

    def listen_topic(self, topic):
        kafka_consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
        kafka_consumer.subscribe([topic])
        for msg in kafka_consumer:
            print(msg)
            kafka_message = self.kafka_message_boundary(msg.value.decode('utf-8'))
            if kafka_message is not None:
                yield kafka_message

    def kafka_message_boundary(self, message_str) -> InputMessage:
        try:
            message_json = json.loads(message_str)
            validate(message_json, self.kafka_input_json_schema)
            return InputMessage(application=message_json["application"], value=message_json["value"],
                                ts_str=message_json["ts"])
        except Exception as e:
            # TODO logs system...
            pass

    def send_output_message(self, topic, message_output):
        message = json.dumps(message_output)
        self.producer.send(topic, bytearray(message, 'utf8'))
