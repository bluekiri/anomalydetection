# -*- coding:utf-8 -*- #

import os
import unittest

from anomalydetection.stream.pubsub_stream_backend import PubSubStreamBackend


class TestPubSubStreamBackend(unittest.TestCase):

    def test(self):

        pubsub = PubSubStreamBackend(
            "bluekiri-bigd-dev-anomdec",
            os.getenv("HOME") + "/Documents/bluekiri-bigd-dev-anomdec.json",
            "test", "test1")

        # Publish
        pubsub.push("hola")

        # Poll
        messages = pubsub.poll()
        if messages:
            for i in messages:
                self.assertEqual("hola", i)
        else:
            raise Exception("Cannot consume published message.")

