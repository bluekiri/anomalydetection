#!/usr/bin/env bash

TIMEOUT=60
HOST=localhost

# Extracted from https://github.com/mrako/wait-for
wait_for() {
  command="$*"
  for i in `seq $TIMEOUT` ; do
    nc -z "$HOST" "$PORT" > /dev/null 2>&1

    result=$?
    if [ $result -eq 0 ] ; then
      if [ -n "$command" ] ; then
        exec $command
      fi
      exit 0
    fi
    sleep 1
  done
  echo "Operation timed out" >&2
  exit 1
}

# Wait for kafka
echo "Waiting for Kafka"
PORT=9092
KAFKA=$(wait_for)

# Wait for PubSub
echo "Waiting for PubSub emulator"
PORT=8085
PUBSUB=$(wait_for)

# Wait for mongo
echo "Waiting for MongoDB"
PORT=27017
MONGO=$(wait_for)
