#!/usr/bin/env bash

# Decrypt secret
openssl aes-256-cbc -K $encrypted_9e5a94a71a40_key -iv $encrypted_9e5a94a71a40_iv -in eco-spirit-208613-5c70334d972b.json.enc -out /tmp/eco-spirit-208613-5c70334d972b.json -d

# Install Spark
cd /tmp
wget http://www-eu.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz
tar xzf spark-2.2.1-bin-hadoop2.7.tgz
ln -s spark-2.2.1-bin-hadoop2.7 spark
