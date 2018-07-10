Deploy
======

.. important::
    Before continue, please read the :ref:`configuration` section, so you will
    need to create a configuration file to start distinct components of the
    framework.

Backend
*******

Start only the backend for the given configuration. This allows you to split the
configuration in small streams chunks to deploy independently to scale
horizontally.

.. code-block:: bash

    export ANOMDEC_HOME=~/anomdec
    anomdec backend

.. code-block:: text

    - anomalydetection.anomdec.Anomdec:35 - INFO - Starting anomdec
    - anomalydetection.anomdec.Anomdec:44 - INFO - Run backend
    ...

Dashboard
*********

Start only the dashboard for the given configuration. Using a unique config
file you are able to visualize all streams.

.. code-block:: bash

    export ANOMDEC_HOME=~/anomdec
    anomdec dashboard

.. code-block:: text

    - anomalydetection.anomdec.Anomdec:35 - INFO - Starting anomdec
    - anomalydetection.anomdec.Anomdec:41 - INFO - Run dashboard
    ...

Embedded
********

You can start it embedded. This will create a subprocess in the dashboard
instance to process the streams.

.. code-block:: bash

    export ANOMDEC_HOME=~/anomdec
    anomdec

.. code-block:: text

    - anomalydetection.anomdec.Anomdec:35 - INFO - Starting anomdec
    - anomalydetection.anomdec.Anomdec:38 - INFO - Run dashboard/backend embedded
    ...