# -*- coding:utf-8 -*- #

import os
import time
import unittest

from anomalydetection.stream.pubsub_stream_backend import PubSubStreamBackend


class TestClient(unittest.TestCase):

    def test_backend(self):
        pubsub = PubSubStreamBackend(
            "bluekiri-bigd-dev-anomdec",
            os.getenv("HOME") + "/Documents/bluekiri-bigd-dev-anomdec.json",
            "test", "test1")
        # Publish
        pubsub.push("hola")

        # Poll
        while True:
            messages = pubsub.poll()
            if messages:
                for i in messages:
                    print(i)
            else:
                time.sleep(0.5)
