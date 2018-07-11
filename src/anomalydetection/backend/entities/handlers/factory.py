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

import importlib

from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.entities.handlers.json import InputJsonMessageHandler


class MessageHandlerFactory(object):

    @staticmethod
    def get_plugin(name) -> BaseMessageHandler:
        module_name = "anomalydetection.backend.entities.handlers.{}".format(name)
        objects = vars(importlib.import_module(module_name))["_objects"]
        for obj in objects:
            if issubclass(obj, BaseMessageHandler):
                return obj()
        raise NotImplementedError()

    @staticmethod
    def get(name) -> BaseMessageHandler:
        def raise_exception():
            raise NotImplementedError()
        func_name = "get_{}".format(name)
        func = getattr(MessageHandlerFactory, func_name, raise_exception)
        try:
            return func()
        except NotImplementedError as ex:
            try:
                return MessageHandlerFactory.get_plugin(name)
            except NotImplementedError as ex:
                raise NotImplementedError(
                    "Calling undefined function: {}.{}()".format(
                        "StreamBuilderFactory", func_name))

    @staticmethod
    def get_json():
        return InputJsonMessageHandler()
