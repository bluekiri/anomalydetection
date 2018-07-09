Configuration
=============

Configuration is statically defined in a YAML file. This section will explain
this file structure.

streams
*******

source / engine
~~~~~~~~~~~~~~~

Streams is the main section of this file. It's a named list that defines how is
a signal processed. It has two required sections, the ``source`` and the ``engine``
This is the minimal configuration to start processing signals but, at this point
we are not persisting the result.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-2,5-16

sink
~~~~

To persist the result we need to add a ``sink``
configuration section.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-2,5-23

repository
~~~~~~~~~~

Repository section could be found in ``sink`` and in ``warmup`` sections, it defines
an storage backend that is supported by :any:`BaseSink` implementations,
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

Full configuration file
***********************

A full example configuration. This configuration reflects a full message flow
reading from a kafka broker, processing with robust detector warmed up with the
same repository that persists the output.

.. literalinclude:: var/config-example.yml
   :linenos:
   :language: yaml
   :lines: 1-
