Plugins
=======

**Anomaly Detection Framework** is extensible by a plugin system.
Plugin files must be placed in ``$ANOMDEC_HOME/plugins`` and are supported
by the configuration parser of ``anomdec.yml`` file.

Interface
*********

To create a plugin you will need to implement the class :any:`Plugin`. You can
implement any *core-around* component, so you can extend functionality as much
as you want.

.. code-block:: python

    class Plugin(object):

        name = None
        # A class in a list derived from BaseConsumerBuilder
        stream_consumer_builders = []
        # A class in a list derived from BaseStreamConsumer
        stream_consumers = []
        # A class in a list derived from BaseProducerBuilder
        stream_producer_builders = []
        # A class in a list derived from BaseStreamProducer
        stream_producers = []
        # A class in a list derived from BaseEngineBuilder
        engine_builders = []
        # A class in a list derived from BaseEngine
        engines = []
        # A class in a list derived from BaseRepositoryBuilder
        repository_builders = []
        # A class in a list derived from BaseRepository
        repositories = []
        # A class in a list derived from BaseMessageHandler
        message_handlers = []


Example
*******

Image you want to implement a new source, so you need to implement the *Builder*
:any:`BaseConsumerBuilder` and the *Consumer* :any:`BaseStreamConsumer`. This
consumer will read messages from a *socket*.

.. code-block:: python

    from anomalydetection.backend.core.plugins import Plugin

    # Needs to be implemented
    class SocketConsumer(BaseStreamConsumer):

        def __init__(self, hostname, port):
            pass

    # This builder is fully implemented, note that the attrs has its own
    # setter in the form of ``set_<attrname>``
    class SocketConsumerBuilder(BaseConsumerBuilder):

        def __init__(self, hostname, port):
            self.set_hostname(hostname)
            self.set_port(port)

        def set_hostname(self, hostname):
            self.hostname = str(hostname)
            return self

        def set_port(self, port):
            self.port = int(port)
            return self

        def build():
            return SocketConsumer(**vars(self).copy())

    class SocketsPlugin(Plugin):
        name = "socket"
        stream_consumer_builders = [SocketConsumerBuilder]
        stream_consumers = [SocketConsumer]

Use in anomdec.yml
******************

The plugin system is fully supported by config parser using the plugin
name in ``type`` sections. And params to the builder are also supported
by ``params`` sections. Here is an example ``anomdec.yml`` file using this
plugin.

.. code-block:: yaml

    version: 1

    streams:

      - name: test
        source:
          type: socket
          params:
            hostname: localhost
            port: 8080
