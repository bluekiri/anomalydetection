Welcome to anomalydetection's documentation!
============================================

.. image:: var/bluekiri_logo.png
   :width: 200

.. warning::
   Anomaly Detection Framework is under an early development phase. API,
   architecture and implementations could suffer important changes.
   For this, Bluekiri do not offer any type of warranty. Use at your
   **own responsibility**.

Status
******

.. image:: https://travis-ci.org/bluekiri/anomalydetection.svg?branch=master
   :target: https://travis-ci.org/bluekiri/anomalydetection
.. image:: https://codecov.io/gh/bluekiri/anomalydetection/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bluekiri/anomalydetection
.. image:: https://img.shields.io/badge/all_contributors-4-blue.svg

Overview
********

This project born from the need of detect anomalies on multiple and completely
different signals, and react to it rapidly. To achieve this, Bluekiri decided to
implement its own system to manage multiple signals at the same time in a easy
and scalable way.

This project is not focused on Machine Learning models, but in an effective
Framework to put those models in production.

Features
********

* It has an abstraction layer to implement engines, streaming sources and sinks,
  repository sources and sinks.

* It supports Kafka and PubSub by default.

* It has a default implementation for that supports tumbling window aggregation
  on Spark, on Kafka and PubSub sources using an specific JSON schema messages.

* Settings are in YAML format.

* It also includes a dashboard to visualize the signal anomalies and play with
  signals in a sandbox to try models, tune parameters an see which parameters
  fits better into your signal.

.. image:: var/dashboard.png

.. note::
   The Sandbox is limited to use the included message handlers and models only.
   Custom models will be available to use after we implement the plugin system.

.. toctree::
   :maxdepth: 4
   :caption: Content

   project
   license
   api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
