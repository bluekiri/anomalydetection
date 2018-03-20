#!/bin/bash

topics=1
while [ $topics -le 1 ]
do
echo "Kafka is not available yet"
topics=`${KAFKA_PATH}/bin/kafka-topics.sh --zookeeper $ZOOKEEPER_HOST --list | wc -l`
sleep 1
done
echo "Kafka is UP!"