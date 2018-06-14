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

import logging
import warnings
from typing import Generator
from multiprocessing import Queue

from kafka import KafkaConsumer, KafkaProducer

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream.aggregation_functions import \
    AggregationFunction
from anomalydetection.backend.stream import BaseStreamBackend, \
    BasePollingStream, BasePushingStream, BaseStreamAggregation
from anomalydetection.common.concurrency import Concurrency
from anomalydetection.common.logging import LoggingMixin


class KafkaPollingStream(BasePollingStream, LoggingMixin):

    def __init__(self,
                 broker_server: str,
                 topic: str,
                 group_id: str) -> None:
        """
        Kafka Stream backend constructor.

        :type broker_server:      str.
        :param broker_server:     broker/s servers.
        :type       topic:        str.
        :param       topic:       topic to read from.
        :type group_id:           str.
        :param group_id:          consumer id.
        """
        super().__init__()
        self.broker_servers = broker_server.split(",")
        self.topic = topic
        self.group_id = group_id

        self.kafka_consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.broker_servers,
            group_id=self.group_id)
        self.kafka_consumer.subscribe([self.topic])

    def poll(self) -> Generator:
        while True:
            self.logger.debug("Polling messages (auto ack). START")
            try:
                for msg in self.kafka_consumer:
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


class KafkaPushingStream(BasePushingStream, LoggingMixin):

    def __init__(self,
                 broker_server: str,
                 output_topic: str) -> None:
        """
        Kafka Stream backend constructor.

        :type broker_server:      str.
        :param broker_server:     broker/s servers.
        :type topic:              str.
        :param topic:             topic to write to.
        """
        super().__init__()
        self.broker_servers = broker_server.split(",")
        self.topic = output_topic

        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.broker_servers,
            api_version=(0, 10))

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            self.kafka_producer.send(self.topic,
                                     bytearray(message, 'utf-8'))
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)

    def __str__(self) -> str:
        return "Kafka topic: brokers: {}, topic: {}".format(
            self.broker_servers,
            self.topic)


class KafkaStreamBackend(BaseStreamBackend, LoggingMixin):

    def __init__(self,
                 broker_server: str,
                 input_topic: str,
                 output_topic: str,
                 group_id: str) -> None:
        """
        Kafka Stream backend constructor.

        :type broker_server:      str.
        :param broker_server:     broker/s servers.
        :type input_topic:        str.
        :param input_topic:       topic to read from.
        :type output_topic:       str.
        :param output_topic:      topic to write to.
        :type group_id:           str.
        :param group_id:          consumer id.
        """
        super().__init__(
            KafkaPollingStream(broker_server,
                               input_topic,
                               group_id),
            KafkaPushingStream(broker_server, output_topic))


class SparkKafkaPollingStream(BasePollingStream,
                              BaseStreamAggregation,
                              LoggingMixin):

    def __init__(self,
                 broker_server: str,
                 topic: str,
                 group_id: str,
                 agg_function: AggregationFunction,
                 agg_window_millis: int) -> None:

        super().__init__(agg_function, agg_window_millis)
        self.broker_servers = broker_server.split(",")
        self.topic = topic
        self.group_id = group_id
        self.queue = Queue()

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
                from pyspark.streaming.kafka import KafkaUtils
                from pyspark.sql.functions import expr

                spark = SparkSession \
                    .builder \
                    .appName("aggr") \
                    .config("spark.jars.packages",
                            "org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.1") \
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

                kafka_stream = KafkaUtils.createDirectStream(
                    ssc,
                    [self.topic],
                    {"metadata.broker.list": ",".join(self.broker_servers)})

                def aggregate_rdd(_queue, _agg, df, ts):

                    if df.first():
                        aggs = df \
                            .groupBy("application") \
                            .agg(_agg.alias("value")) \
                            .collect()

                        for row in aggs:
                            logging.debug("Pushing message to queue")
                            _queue.put(
                                InputMessage(row["application"],
                                             value=row["value"],
                                             ts=ts).to_json())
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
        return "Kafka aggregated topic: " \
               "brokers: {}, topic: {}, func: {}, window: {}ms".format(
                    self.broker_servers,
                    self.topic,
                    self.agg_function.name,
                    self.agg_window_millis)


class SparkKafkaStreamBackend(BaseStreamBackend, LoggingMixin):

    def __init__(self,
                 broker_server: str,
                 input_topic: str,
                 output_topic: str,
                 group_id: str,
                 agg_function: AggregationFunction,
                 agg_window_millis: int) -> None:

        super().__init__(
            SparkKafkaPollingStream(broker_server,
                                    input_topic,
                                    group_id,
                                    agg_function,
                                    agg_window_millis),
            KafkaPushingStream(broker_server, output_topic))
