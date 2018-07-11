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
import sys
from collections import OrderedDict

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.engine.cad_engine import CADDetector
from anomalydetection.backend.engine.ema_engine import EMADetector
from anomalydetection.backend.engine.robust_z_engine import RobustDetector


class BaseEngineBuilder(object):
    """
    BaseBuilder, implement this to create Engine Builders.
    """

    def build(self) -> BaseEngine:
        """
        Build the engine

        :return:  A BaseEngine implementation instance.
        """
        raise NotImplementedError("To implement in child classes.")

    def set(self, name: str, value: str):
        def raise_exception(*args, **kwargs):
            raise NotImplementedError()
        func_name = "set_{}".format(name)
        func = getattr(self, func_name, raise_exception)
        try:
            return func(value)
        except NotImplementedError as ex:
            raise NotImplementedError(
                "Calling undefined function: {}.{}()".format(
                    self.__class__.__name__, func_name))


class CADDetectorBuilder(BaseEngineBuilder):

    type = "cad"

    def __init__(self,
                 min_value=-sys.maxsize,
                 max_value=sys.maxsize,
                 threshold=0.95,
                 rest_period=30,
                 max_left_semi_contexts_length=8,
                 max_active_neurons_num=16,
                 num_norm_value_bits=3):
        self.min_value = min_value
        self.max_value = max_value
        self.threshold = threshold
        self.rest_period = rest_period
        self.max_left_semi_contexts_length = max_left_semi_contexts_length
        self.max_active_neurons_num = max_active_neurons_num
        self.num_norm_value_bits = num_norm_value_bits

    def set_min_value(self, value):
        self.min_value = int(value)
        return self

    def set_max_value(self, value):
        self.max_value = int(value)
        return self

    def set_threshold(self, threshold):
        self.threshold = float(threshold)
        return self

    def set_rest_period(self, rest_period):
        self.rest_period = int(rest_period)
        return self

    def set_max_left_semi_contexts_length(self, max_left_semi_contexts_length):
        self.max_left_semi_contexts_length = int(max_left_semi_contexts_length)
        return self

    def set_max_active_neurons_num(self, max_active_neurons_num):
        self.max_active_neurons_num = int(max_active_neurons_num)
        return self

    def set_num_norm_value_bits(self, num_norm_value_bits):
        self.num_norm_value_bits = int(num_norm_value_bits)
        return self

    def build(self) -> CADDetector:
        return CADDetector(**vars(self).copy())


class RobustDetectorBuilder(BaseEngineBuilder):

    type = "robust"

    def __init__(self, window=100, threshold=0.9999):
        self.window = window
        self.threshold = threshold

    def set_window(self, window):
        self.window = int(window)
        return self

    def set_threshold(self, threshold):
        self.threshold = float(threshold)
        return self

    def build(self) -> RobustDetector:
        return RobustDetector(**vars(self).copy())


class EMADetectorBuilder(BaseEngineBuilder):

    type = "ema"

    def __init__(self, window=100, threshold=0.9999):
        self.window = window
        self.threshold = threshold

    def set_window(self, window):
        self.window = int(window)
        return self

    def set_threshold(self, threshold):
        self.threshold = float(threshold)
        return self

    def build(self) -> EMADetector:
        return EMADetector(**vars(self).copy())


class EngineBuilderFactory(object):

    engines = OrderedDict()

    @classmethod
    def register_engine(cls, key, class_name):
        cls.engines[key] = {"key": key, "name": class_name}

    @staticmethod
    def get_plugin(name) -> BaseEngineBuilder:
        module_name = "anomalydetection.backend.engine.{}_builder".format(name)
        objects = vars(importlib.import_module(module_name))["_objects"]
        for obj in objects:
            if issubclass(obj, BaseEngineBuilder):
                return obj()
        raise NotImplementedError()

    @staticmethod
    def get(name) -> BaseEngineBuilder:
        def raise_exception():
            raise NotImplementedError()
        func_name = "get_{}".format(name)
        func = getattr(EngineBuilderFactory, func_name, raise_exception)
        try:
            return func()
        except NotImplementedError as ex:
            try:
                return EngineBuilderFactory.get_plugin(name)
            except NotImplementedError as ex:
                raise NotImplementedError(
                    "Calling undefined function: {}.{}()".format(
                        "EngineBuilderFactory", func_name))

    @staticmethod
    def get_robust() -> RobustDetectorBuilder:
        return RobustDetectorBuilder()

    @staticmethod
    def get_cad() -> CADDetectorBuilder:
        return CADDetectorBuilder()

    @staticmethod
    def get_ema() -> EMADetectorBuilder:
        return EMADetectorBuilder()


EngineBuilderFactory.register_engine("robust", "RobustDetector")
EngineBuilderFactory.register_engine("cad", "CADDetector")
EngineBuilderFactory.register_engine("ema", "EMADetector")
