#!/usr/bin/env bash

# Pull images before call docker-compose
docker pull mongo:3.6-jessie
docker pull google/cloud-sdk:latest
docker pull wurstmeister/kafka:2.11-1.1.0
docker pull wurstmeister/zookeeper:3.4.6

# Start
docker-compose up &
