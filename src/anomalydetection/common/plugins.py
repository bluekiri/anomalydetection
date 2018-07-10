# -*- coding:utf-8 -*- #
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import inspect
import logging
import os
import re
import sys
from importlib.machinery import SourceFileLoader
from types import ModuleType

from anomalydetection.backend.engine.builder import EngineBuilderFactory


class Plugin(object):

    name = None
    stream_consumer_builders = []  # Implements BaseConsumerBuilder
    stream_consumers = []          # Implements BaseStreamConsumer
    stream_producer_builders = []  # Implements BaseProducerBuilder
    stream_producers = []          # Implements BaseStreamProducer
    engine_builders = []           # Implements BaseEngineBuilder
    engines = []                   # Implements BaseEngine
    repository_builders = []       # Implements BaseRepositoryBuilder
    repositories = []              # Implements BaseRepository
    message_handlers = []          # Implements BaseMessageHandler

    @staticmethod
    def validate():
        return True


plugins = []

# Plugins folder
plugins_folder = os.getenv("ANOMDEC_HOME", os.environ["HOME"] + "/anomdec")
plugins_folder += "/plugins"

norm_pattern = re.compile(r'[/|.]')

for root, dirs, files in os.walk(plugins_folder, followlinks=True):
    for f in files:
        try:
            filepath = os.path.join(root, f)
            if not os.path.isfile(filepath):
                continue
            mod_name, file_ext = os.path.splitext(
                os.path.split(filepath)[-1])
            if file_ext != '.py':
                continue

            logging.debug("Importing plugin modules, {}".format(filepath))
            namespace = '_'.join([re.sub(norm_pattern, '__', root), mod_name])

            m = SourceFileLoader(namespace, filepath).load_module()
            for obj in list(m.__dict__.values()):
                if (inspect.isclass(obj) and issubclass(obj, Plugin)
                        and obj is not Plugin):
                    obj.validate()
                    if obj not in plugins:
                        plugins.append(obj)

        except Exception as e:
            logging.exception(e)
            logging.error('Failed to import plugin %s', filepath)


def make_module(name, objects):
    logging.debug('Creating module %s', name)
    name = name.lower()
    module = ModuleType(name)
    module._name = name.split('.')[-1]
    module._objects = objects
    module.__dict__.update((o.__name__, o) for o in objects)
    return module


stream_builders = []           # Implements BaseConsumerBuilder/BaseProducerBuilder
streams = []                   # Implements BaseStreamConsumer/BaseStreamProducer
engine_builders = []           # Implements BaseEngineBuilder
engines = []                   # Implements BaseEngine
repository_builders = []       # Implements BaseRepositoryBuilder
repositories = []              # Implements BaseRepository
message_handlers = []          # Implements BaseMessageHandler

for p in plugins:

    # Stream
    stream_builders.append(
        make_module("anomalydetection.backend.stream.{}_builder".format(p.name),
                    p.stream_consumer_builders + p.stream_producer_builders))

    streams.append(
        make_module("anomalydetection.backend.stream.{}".format(p.name),
                    p.stream_consumer_builders + p.stream_producers))

    # Engine
    engine_builders.append(
        make_module("anomalydetection.backend.engine.{}_builder".format(p.name),
                    p.engine_builders))

    engines.append(
        make_module("anomalydetection.backend.engine.{}".format(p.name),
                    p.engines))

    # Repository
    repository_builders.append(
        make_module("anomalydetection.backend.repository.{}_builder".format(p.name),
                    p.repository_builders))

    repositories.append(
        make_module("anomalydetection.backend.repository.{}".format(p.name),
                    p.repositories))

    # Message handlers
    message_handlers.append(
        make_module("anomalydetection.backend.entities.handlers.{}".format(p.name),
                    p.message_handlers)
    )

for stream in streams:
    sys.modules[stream.__name__] = stream

for str_builder in stream_builders:
    sys.modules[str_builder.__name__] = str_builder

for repository in repositories:
    sys.modules[repository.__name__] = repository

for repo_builder in repository_builders:
    sys.modules[repo_builder.__name__] = repo_builder

for engine in engines:
    sys.modules[engine.__name__] = engine
    # It is necessary to view in dashboard
    EngineBuilderFactory.register_engine(engine._name, engine._name)

for eng_builder in engine_builders:
    sys.modules[eng_builder.__name__] = eng_builder

for message_handler in message_handlers:
    sys.modules[message_handler.__name__] = message_handler
