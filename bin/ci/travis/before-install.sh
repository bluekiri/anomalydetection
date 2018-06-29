#!/usr/bin/env bash

cd /tmp
wget http://www-eu.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz
tar vxzf spark-2.2.1-bin-hadoop2.7.tgz
ln -s spark-2.2.1-bin-hadoop2.7 spark