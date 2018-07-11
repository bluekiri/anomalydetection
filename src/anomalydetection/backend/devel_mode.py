# -*- coding:utf-8 -*- #
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import random

from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from rx import Observable, Observer

from anomalydetection.backend.stream.builder import StreamBuilderFactory
from anomalydetection.backend.core.config import Config


class DevelConfigWrapper(Config):

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.mode = str(config.mode)
        self.config = config.config.copy()

    def build_producers(self):

        producers = []
        project = "testing"
        try:

            # Create pubsub topics
            publisher = PublisherClient()
            publisher.create_topic(
                publisher.topic_path(project,
                                     "test10"))
            publisher.create_topic(
                publisher.topic_path(project,
                                     "test20"))

            # Create pubsub subscriptions
            subscriber = SubscriberClient()
            subscriber.create_subscription(
                subscriber.subscription_path(project, "test10"),
                subscriber.topic_path(project, "test10"))
            subscriber.create_subscription(
                subscriber.subscription_path(project, "test20"),
                subscriber.topic_path(project, "test20"))

        except AlreadyExists as _:
                    pass

        producers.append(
            StreamBuilderFactory.get_producer_pubsub()
                                .set_project_id(project)
                                .set_output_topic("test10").build())
        producers.append(
            StreamBuilderFactory.get_producer_kafka()
                                .set_broker_servers("localhost:9092")
                                .set_output_topic("test1").build())

        producers.append(
            StreamBuilderFactory.get_producer_kafka()
                                .set_broker_servers("localhost:9092")
                                .set_output_topic("test3").build())

        return producers


def produce_messages(config: Config):

    vals = [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9] + \
           [12, 23, 40, 51, 100]  # <- Anomalies

    apps = ["devel0", "devel1", "devel2"]

    class IntervalObserver(Observer):

        def __init__(self, publisher) -> None:
            super().__init__()
            self.publisher = publisher

        def push(self):
            from datetime import datetime
            for app in apps:
                random.shuffle(vals)
                self.publisher.push(json.dumps({
                    "application": app,
                    "ts": str(datetime.now()),
                    "value": vals[0]
                }))

        def on_next(self, value):
            return self.push()

        def on_error(self, error):
            return super().on_error(error)

        def on_completed(self):
            return super().on_completed()

    # Send a message each 5s
    publishers = DevelConfigWrapper(config).build_producers()
    for pub in publishers:
        Observable.interval(5000).subscribe(IntervalObserver(pub))
