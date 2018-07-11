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
import warnings
from typing import Generator
from multiprocessing import Queue as MultiprocessingQueue
from queue import Queue as Queue

from kafka import KafkaConsumer, KafkaProducer

from anomalydetection import BASE_PATH
from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream import BaseStreamAggregation
from anomalydetection.backend.stream import BaseStreamConsumer
from anomalydetection.backend.stream import BaseStreamProducer
from anomalydetection.backend.stream.agg.functions import AggregationFunction
from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.logging import LoggingMixin


class KafkaStreamConsumer(BaseStreamConsumer, LoggingMixin):

    def __init__(self,
                 broker_servers: str,
                 input_topic: str,
                 group_id: str) -> None:
        """
        KafkaStreamConsumer constructor

        :param broker_servers:     broker servers
        :param input_topic:       input topic
        :param group_id:          consumer group id
        """
        super().__init__()
        self.broker_servers = broker_servers.split(",")
        self.topic = input_topic
        self.group_id = group_id
        self.subscribed = True

        self._kafka_consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.broker_servers,
            group_id=self.group_id)
        self._kafka_consumer.subscribe([self.topic])

    def unsubscribe(self):
        self.subscribed = False
        self._kafka_consumer.unsubscribe()

    def poll(self) -> Generator:
        while self.subscribed:
            self.logger.debug("Polling messages (auto ack). START")
            try:
                for msg in self._kafka_consumer:
                    message = msg.value.decode('utf-8')
                    self.logger.debug("Message received: {}".format(message))
                    yield message
            except Exception as ex:
                self.logger.error("Error polling messages.", ex)

            self.logger.debug("Polling messages. END")

    def __str__(self) -> str:
        return "Kafka topic: brokers: {}, topic: {}".format(
            self.broker_servers,
            self.topic)


class KafkaStreamProducer(BaseStreamProducer, LoggingMixin):

    def __init__(self,
                 broker_servers: str,
                 output_topic: str) -> None:
        """
        KafkaStreamProducer constructor

        :param broker_servers:     broker servers
        :param output_topic:      topic to write to
        """
        super().__init__()
        self.broker_servers = broker_servers.split(",")
        self.output_topic = output_topic

        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.broker_servers,
            api_version=(0, 10))

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            self.kafka_producer.send(self.output_topic,
                                     bytearray(message, 'utf-8'))
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)

    def __str__(self) -> str:
        return "Kafka topic: brokers: {}, topic: {}".format(
            self.broker_servers,
            self.output_topic)


class SparkKafkaStreamConsumer(BaseStreamConsumer,
                               BaseStreamAggregation,
                               LoggingMixin):

    def __init__(self,
                 broker_servers: str,
                 input_topic: str,
                 group_id: str,
                 agg_function: AggregationFunction,
                 agg_window_millis: int,
                 spark_opts: dict={},
                 multiprocessing=True) -> None:
        """
        SparkKafkaStreamConsumer constructor

        :param broker_servers:      broker servers
        :param input_topic:         input topic
        :param group_id:            consumer group id
        :param agg_function:        aggregation function to apply
        :param agg_window_millis:   aggregation window in milliseconds
        :param spark_opts:          spark options dict
        :param multiprocessing:     use multiprocessing instead of threading
        """
        super().__init__(agg_function, agg_window_millis)
        self.broker_servers = broker_servers.split(",")
        self.input_topic = input_topic
        self.group_id = group_id
        self.spark_opts = spark_opts
        self.subscribed = True
        self.multiprocessing = multiprocessing
        if self.multiprocessing:
            self.queue = MultiprocessingQueue()
        else:
            self.queue = Queue()

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
                from pyspark.streaming.kafka import KafkaUtils
                from pyspark.sql.functions import expr, window

                spark_builder = SparkSession \
                    .builder \

                for k in _spark_opts:
                    spark_builder = spark_builder.config(k, _spark_opts[k])

                spark_builder = spark_builder \
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

                kafka_stream = KafkaUtils.createDirectStream(
                    ssc,
                    [self.input_topic],
                    {"metadata.broker.list": ",".join(self.broker_servers)})

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
                        warnings.warn("Empty RDD")

                # Create kafka stream
                kafka_stream \
                    .map(lambda x: x[1]) \
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
        return "Kafka aggregated topic: " \
               "brokers: {}, topic: {}, func: {}, window: {}ms".format(
                    self.broker_servers,
                    self.input_topic,
                    self.agg_function.name,
                    self.agg_window_millis)
