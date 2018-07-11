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
from multiprocessing import Queue as MultiprocessingQueue
from queue import Queue as Queue

from anomalydetection import BASE_PATH
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream.agg.functions import AggregationFunction
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
        """
        PubSubStreamConsumer constructor

        :param project_id:     the project id
        :param subscription:   the subscription name
        :param auth_file:      path to credentials json file
        """
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
        self.subscribed = True

    def _full_subscription_name(self):
        return "projects/{}/{}/{}".format(self.project_id,
                                          "subscriptions",
                                          self.subscription)

    def __enqueue(self, message: Message) -> None:
        self.logger.debug(
            "Message received: {}".format(str(message.data, "utf-8")))
        self.queue.put(message)

    def __dequeue(self) -> Message:
        return self.queue.get(timeout=1)

    def unsubscribe(self):
        self.subscribed = False

    def poll(self) -> Generator:
        while self.subscribed:
            try:
                message = self.__dequeue()
                message.ack()
                yield str(message.data, "utf-8")
            except Exception:
                pass

    def __str__(self) -> str:
        return "PubSub subscription: {}".format(self._full_subscription_name())


class PubSubStreamProducer(BaseStreamProducer, LoggingMixin):

    def __init__(self,
                 project_id: str,
                 output_topic: str,
                 auth_file: str = None) -> None:
        """
        PubSubStreamConsumer constructor

        :param project_id:     the project id
        :param output_topic:   the topic to push the messages to
        :param auth_file:      path to credentials json file
        """
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
                 auth_file: str = None,
                 spark_opts: dict={},
                 multiprocessing=False) -> None:
        """
        SparkPubSubStreamConsumer constructor

        :param project_id:          the project id
        :param subscription:        the subscription name
        :param agg_function:        aggregation function to apply
        :param agg_window_millis:   aggregation window in milliseconds
        :param auth_file:           path to credentials json file
        :param spark_opts:          spark options dict
        :param multiprocessing:     use multiprocessing instead of threading
        """
        super().__init__(agg_function, agg_window_millis)
        self.project_id = project_id
        self.subscription = subscription
        self.spark_opts = spark_opts
        self.subscribed = True
        self.multiprocessing = multiprocessing
        if self.multiprocessing:
            self.queue = MultiprocessingQueue()
        else:
            self.queue = Queue()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_file

        def run_spark_job(queue: Queue,
                          _agg_function: AggregationFunction,
                          _agg_window_millis: int,
                          _spark_opts: dict = {},
                          _environment: dict = {}):
            os.environ.update(_environment)
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
                from pyspark.sql.functions import expr, window
                from pyspark.serializers import NoOpSerializer
                from pyspark.streaming import DStream
                from pyspark.streaming.kafka import utf8_decoder

                spark_builder = SparkSession \
                    .builder \

                for k in _spark_opts:
                    spark_builder = spark_builder.config(k, _spark_opts[k])

                spark_builder \
                    .appName(str(self)) \
                    .config("spark.jars.packages",
                            "org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.1,"
                            "org.apache.bahir:spark-streaming-pubsub_2.11:2.2.1") \
                    .config("spark.jars",
                            BASE_PATH + "/lib/streaming-pubsub-serializer_2.11-0.1.jar")

                spark = spark_builder.getOrCreate()
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

                deserializer = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.SparkPubsubMessageSerializer()  # noqa: E501
                pubsub_utils = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.PubsubUtils
                credentials = \
                    ssc._jvm.org.apache.spark.streaming.pubsub.SparkGCPCredentials
                storage_level = \
                    ssc._jvm.org.apache.spark.storage.StorageLevel

                _pubsub_stream = pubsub_utils \
                    .createStream(ssc._jssc,
                                  project_id,
                                  subscription,
                                  credentials.Builder().build(),
                                  storage_level.DISK_ONLY())
                _pubsub_stream_des = _pubsub_stream.transform(deserializer)
                ser = NoOpSerializer()
                pubsub_stream = DStream(_pubsub_stream_des, ssc, ser).map(utf8_decoder)

                def aggregate_rdd(_queue, _agg, df, ts):

                    secs = int(self.agg_window_millis / 1000)
                    win = window("ts",
                                 "{}  seconds".format(secs))
                    if df.first():
                        aggs = df \
                            .groupBy("application", win) \
                            .agg(_agg.alias("value")) \
                            .collect()

                        for row in aggs:
                            message = InputMessage(row["application"],
                                                   value=row["value"],
                                                   ts=ts)
                            self.logger.debug(
                                "Enqueue: {}".format(message.to_json()))
                            try:
                                _queue.put(message.to_json())
                            except AssertionError as ex:
                                self.logger.warn(str(ex))
                    else:
                        self.logger.warn("Empty RDD")

                # Create kafka stream
                pubsub_stream \
                    .foreachRDD(lambda ts, rdd:
                                aggregate_rdd(queue, agg,
                                              spark.read.json(rdd), ts))

                # Run
                ssc.start()
                if "timeout" in _spark_opts:
                    ssc.awaitTerminationOrTimeout(_spark_opts["timeout"])
                    ssc.stop()
                    spark.stop()
                else:
                    ssc.awaitTermination()
                    ssc.stop()
                    spark.stop()

            except Exception as e:
                raise e

        # Run in multiprocessing, each aggregation runs a spark driver.
        runner = Concurrency.run_process \
            if self.multiprocessing \
            else Concurrency.run_thread

        Concurrency.get_lock("spark").acquire()
        pid = runner(target=run_spark_job,
                     args=(self.queue,
                           self.agg_function,
                           self.agg_window_millis,
                           self.spark_opts,
                           os.environ.copy()),
                     name="PySpark {}".format(str(self)))
        Concurrency.schedule_release("spark", 30)
        self.pid = pid

    def unsubscribe(self):
        self.subscribed = False
        if isinstance(self.queue, MultiprocessingQueue):
            self.queue.close()
            self.queue.join_thread()
        elif isinstance(self.queue, Queue):
            self.queue.join()

    def poll(self) -> Generator:
        while self.subscribed:
            try:
                message = self.queue.get(timeout=2)
                yield message
            except Exception as _:
                pass

    def __str__(self) -> str:
        return "PubSub aggregated subscription: " \
               "project: {}, subscription: {}, func: {}, window: {}ms".format(
                    self.project_id,
                    self.subscription,
                    self.agg_function.name,
                    self.agg_window_millis)
