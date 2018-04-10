# -*- coding:utf-8 -*-

from anomalydetection.stream.pubsub_stream_backend import PubSubStreamBackend
from anomalydetection.conf import *

class StreamFactory(object):

    def create_pubsub_stream(self):
        return PubSubStreamBackend(
            PUBSUB_PROJECT_ID,
            PUBSUB_TOPIC
        )
