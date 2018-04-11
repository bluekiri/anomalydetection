# -*- coding:utf-8 -*- #

import unittest

from anomalydetection.stream.kafka_stream_backend import KafkaStreamBackend


class TestPubSubStreamBackend(unittest.TestCase):

    def test(self):

        kafka = KafkaStreamBackend("192.168.1.141:9094", "192.168.1.141:9094", "TEST1", "TEST1", "test1")

        # Publish
        kafka.push("hola")

        # Poll
        messages = kafka.poll()
        if messages:
            for i in messages:
                self.assertEqual("hola", i)
                kafka.kafka_consumer.unsubscribe()
        else:
            raise Exception("Cannot consume published message.")

