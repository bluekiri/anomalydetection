# -*- coding:utf-8 -*-

import logging
from typing import Generator

from kafka import KafkaConsumer, KafkaProducer

from anomalydetection.stream import StreamBackend


class KafkaStreamBackend(StreamBackend):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self,
                 bootstrap_server: str,
                 broker_server: str,
                 input_topic: str,
                 output_topic: str,
                 group_id: str) -> None:
        """
        Kafka Stream backend constructor.

        :type bootstrap_server:   str.
        :param bootstrap_server:  bootstrap server/s.
        :type broker_server:      str.
        :param broker_server:     broker/s servers.
        :type input_topic:        str.
        :param input_topic:       topic to read from.
        :type output_topic:       str.
        :param output_topic:      topic to write to.
        :type group_id:           str.
        :param group_id:          consumer id.
        """
        super().__init__()
        self.bootstrap_servers = bootstrap_server.split(",")
        self.broker_servers = broker_server.split(",")
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id

        self.kafka_consumer = KafkaConsumer(
            self.input_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id)
        self.kafka_consumer.subscribe([self.input_topic])

        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.broker_servers,
            api_version=(0, 10))

    def poll(self) -> Generator:
        while True:
            self.logger.debug("Polling messages (auto ack). START")
            try:
                for msg in self.kafka_consumer:
                    yield msg.value.decode('utf-8')
            except Exception as ex:
                self.logger.error("Error polling messages.", ex)

            self.logger.debug("Polling messages. END")

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message. START")
            self.kafka_producer.send(self.output_topic,
                                     bytearray(message, 'utf-8'))
            self.logger.debug("Pushing message. END")
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)
