# -*- coding:utf-8 -*-

import logging
import threading
import warnings
from queue import Queue
from typing import Generator

from kafka import KafkaConsumer, KafkaProducer

from anomalydetection.backend.entities.input_message import InputMessage
from anomalydetection.backend.stream.aggregation_functions import \
    AggregationFunction
from anomalydetection.backend.stream import BaseStreamBackend


class KafkaStreamBackend(BaseStreamBackend):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

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
        super().__init__()
        self.broker_servers = broker_server.split(",")
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id

        self.kafka_consumer = KafkaConsumer(
            self.input_topic,
            bootstrap_servers=self.broker_servers,
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
                    message = msg.value.decode('utf-8')
                    self.logger.debug("Message received: {}".format(message))
                    yield message
            except Exception as ex:
                self.logger.error("Error polling messages.", ex)

            self.logger.debug("Polling messages. END")

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            self.kafka_producer.send(self.output_topic,
                                     bytearray(message, 'utf-8'))
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)


class SparkKafkaStreamBackend(BaseStreamBackend):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self,
                 broker_server: str,
                 input_topic: str,
                 output_topic: str,
                 group_id: str,
                 agg_function: AggregationFunction,
                 agg_window_millis: int) -> None:

        super().__init__(agg_function, agg_window_millis)
        self.broker_servers = broker_server.split(",")
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.queue = Queue()

        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.broker_servers,
            api_version=(0, 10))

        def helper(queue: Queue,
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
                    [self.input_topic],
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

        # Run in thread.
        p = threading.Thread(target=helper,
                             args=(self.queue,
                                   self.agg_function,
                                   self.agg_window_millis),
                             name="PySpark")
        p.start()

    def poll(self) -> Generator:
        while True:
            message = self.queue.get()
            yield message

    def push(self, message: str) -> None:
        try:
            self.logger.debug("Pushing message: {}.".format(message))
            self.kafka_producer.send(self.output_topic,
                                     bytearray(message, 'utf-8'))
        except Exception as ex:
            self.logger.error("Pushing message failed.", ex)
