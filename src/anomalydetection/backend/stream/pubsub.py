# -*- coding:utf-8 -*-
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

import os
from collections import Generator
from queue import Queue

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream.aggregation_functions import AggregationFunction
from google.cloud.pubsub_v1.subscriber.message import Message
from google.cloud import pubsub

from anomalydetection.backend.stream import BaseStreamAggregation
from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.backend.stream import BaseStreamProducer
from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.logging import LoggingMixin


class PubSubStreamConsumer(BaseStreamConsumer, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 subscription: str,
                 auth_file: str = None) -> None:

        super().__init__()
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.subscription = subscription
        self.queue = Queue()
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        self.subs = self.subscriber.subscribe(self._full_subscription_name(),
                                              callback=self.__enqueue)

    def _full_subscription_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "subscriptions",
                                          self.subscription)

    def __enqueue(self, message: Message) -> None:
        self.logger.debug(
            "Message received: {}".format(str(message.data, "utf-8")))
        self.queue.put(message)

    def __dequeue(self) -> Message:
        return self.queue.get()

    def poll(self) -> Generator:
        while True:
            message = self.__dequeue()
            message.ack()
            yield str(message.data, "utf-8")

    def __str__(self) -> str:
        return "PubSub subscription: {}".format(self._full_subscription_name())


class PubSubStreamProducer(BaseStreamProducer, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 output_topic: str,
                 auth_file: str = None) -> None:

        super().__init__()
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.output_topic = output_topic
        self.queue = Queue()
        self.publisher = pubsub.PublisherClient()

    def _full_topic_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "topics",
                                          self.output_topic)

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            encoded = message.encode("utf-8")
            self.publisher.publish(self._full_topic_name(), encoded)
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)

    def __str__(self) -> str:
        return "PubSub topic: {}".format(self._full_topic_name())


class SparkPubsubStreamConsumer(BaseStreamConsumer,
                                BaseStreamAggregation,
                                LoggingMixin):

    def __init__(self,
                 project_id: str,
                 subscription: str,
                 agg_function: AggregationFunction,
                 agg_window_millis: int,
                 auth_file: str = None) -> None:

        super().__init__(agg_function, agg_window_millis)
        if auth_file:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS", auth_file)
        self.project_id = project_id
        self.subscription = subscription
        self.queue = Queue()

        # FIXME: This is not working because the RDD type.
        def run_spark_job(queue: Queue,
                          _agg_function: AggregationFunction,
                          _agg_window_millis: int):
            try:
                try:
                    import findspark
                    findspark.init()
                except Exception as ex:
                    self.logger.warn("Cannot import Spark pyspark with"
                                     " findspark. Message: {}".format(str(ex)))
                    pass

                from pyspark.sql import SparkSession
                from pyspark.streaming import StreamingContext
                from pyspark.sql.functions import expr
                from pyspark.serializers import NoOpSerializer
                from pyspark.streaming import DStream

                spark = SparkSession \
                    .builder \
                    .appName(str(self)) \
                    .config("spark.jars", "") \
                    .config("spark.jars.packages",
                            "org.apache.bahir:spark-streaming-pubsub_2.11:2.2.1") \
                    .getOrCreate()

                spark.sparkContext.setLogLevel("WARN")
                ssc = StreamingContext(spark.sparkContext,
                                       (agg_window_millis / 1000))

                agg = expr("value")
                if _agg_function == AggregationFunction.AVG:
                    agg = expr("avg(value)")
                elif _agg_function == AggregationFunction.SUM:
                    agg = expr("sum(value)")
                elif _agg_function == AggregationFunction.COUNT:
                    agg = expr("count(value)")
                elif _agg_function == AggregationFunction.P50:
                    agg = expr("percentile(value, 0.5)")
                elif _agg_function == AggregationFunction.P75:
                    agg = expr("percentile(value, 0.75)")
                elif _agg_function == AggregationFunction.P95:
                    agg = expr("percentile(value, 0.95)")
                elif _agg_function == AggregationFunction.P99:
                    agg = expr("percentile(value, 0.99)")

                pubsub_utils = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.PubsubUtils
                credentials = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.SparkGCPCredentials
                storage_level = \
                    ssc._jvm.org.apache.spark.storage.StorageLevel
                deserializer = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.SparkPubsubMessageSerializer()  # noqa: E501

                _pubsub_stream = pubsub_utils \
                    .createStream(ssc._jssc,
                                  project_id,
                                  subscription,
                                  credentials.Builder().build(),
                                  storage_level.DISK_ONLY())
                _pubsub_stream_des = _pubsub_stream.transform(deserializer)
                ser = NoOpSerializer()
                pubsub_stream = DStream(_pubsub_stream_des, ssc, ser)

                def aggregate_rdd(_queue, _agg, df, ts):

                    if df.first():
                        aggs = df \
                            .groupBy("application") \
                            .agg(_agg.alias("value")) \
                            .collect()

                        for row in aggs:
                            self.logger.debug("Pushing message to queue")
                            _queue.put(
                                InputMessage(row["application"],
                                             value=row["value"],
                                             ts=ts).to_json())
                    else:
                        self.logger.warn("Empty RDD")

                # Create kafka stream
                pubsub_stream \
                    .map(lambda x: x[1]) \
                    .foreachRDD(lambda ts, rdd:
                                aggregate_rdd(queue, agg,
                                              spark.read.json(rdd), ts))

                # Run
                ssc.start()
                ssc.awaitTermination()

            except Exception as e:
                print("Error importing pyspark", e)
                exit(127)

        # Run in multiprocessing, each aggregation runs a spark driver.
        Concurrency.run_process(target=run_spark_job,
                                args=(self.queue,
                                      self.agg_function,
                                      self.agg_window_millis),
                                name="PySpark {}".format(str(self)))

    def poll(self) -> Generator:
        while True:
            message = self.queue.get()
            yield message

    def __str__(self) -> str:
        return "PubSub aggregated subscription: " \
               "project: {}, subscription: {}, func: {}, window: {}ms".format(
                    self.project_id,
                    self.subscription,
                    self.agg_function.name,
                    self.agg_window_millis)
