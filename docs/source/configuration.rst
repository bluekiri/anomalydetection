.. _configuration:

Configuration
=============

Configuration is statically defined in a YAML file. The application reads
``anomdec.yml`` from ``$ANOMDEC_HOME`` path. The following section describes
this file structure.

streams
*******

``Streams`` is the main section of this file. It's a named list that defines how
is a signal processed.

source / engine
~~~~~~~~~~~~~~~

It has two required sections, the ``source`` and the ``engine``
This is the minimal configuration to start processing signals but, at this point
we are not persisting the result.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-2,5-16

sink
~~~~

To persist the result we need to add a ``sink`` configuration section. This can
be a list of *sinks*.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-2,5-30

warmup
~~~~~~

``warmup`` section has two roles, the first is to be used to *warm up* the
engine before starting making predictions. The second one is to make the data
accessible from the dashboard to visualize it. We will define a ``warmup``
configuration section with one ``repository`` that is also used in ``sink``.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-2,5-

repository
~~~~~~~~~~

Repository section could be found in ``sink`` and in ``warmup`` sections, it
defines an storage backend that is supported by :any:`BaseSink` implementations,
:any:`RepositorySink` and :any:`ObservableRepository` respectively.


That ``sink`` repository could be also used as ``warmup`` to *warm up* the model
in case of a model that require previous data to evaluate new data. *Although it
is defined as a list, only the first element will be used to warm up the model.*


.. literalinclude:: var/config-example.yml
    :linenos:
    :language: yaml
    :lines: 26-29
    :dedent: 8

websocket
*********

There is a ``websocket`` section that is used to send output ``ticks`` to the
dashboard. This allows to update dashboard plots in realtime.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 3

Example configuration file
**************************

anomdec.yml
~~~~~~~~~~~

A full example configuration. This configuration reflects a full message flow
reading from a kafka broker, processing with robust detector warmed up with the
same repository that persists the output.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-

diagram
~~~~~~~

Here it is a diagram that represents the full configuration file. We can see
that the output of the engine could be *sinked* to a repository and to an
streaming system to visualize and react for anomalies, and is also used to
*warm up* the engine in case of restart or failure.

.. image:: var/config-example.svg