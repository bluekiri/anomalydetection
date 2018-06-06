# -*- conding:utf-8 -*- #
import sys
from collections import OrderedDict

from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.engine.cad_engine import CADDetector
from anomalydetection.backend.engine.robust_z_engine import RobustDetector


class BaseBuilder(object):

    def build(self) -> BaseEngine:
        raise NotImplementedError("To implement on child classes.")


class CADDetectorBuilder(BaseBuilder):

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
        self.min_value = value
        return self

    def set_max_value(self, value):
        self.max_value = value
        return self

    def set_threshold(self, threshold):
        self.threshold = threshold
        return self

    def set_rest_period(self, rest_period):
        self.rest_period = rest_period
        return self

    def set_max_left_semi_contexts_length(self, max_left_semi_contexts_length):
        self.max_left_semi_contexts_length = max_left_semi_contexts_length
        return self

    def set_max_active_neurons_num(self, max_active_neurons_num):
        self.max_active_neurons_num = max_active_neurons_num
        return self

    def set_num_norm_value_bits(self, num_norm_value_bits):
        self.num_norm_value_bits = num_norm_value_bits
        return self

    def build(self) -> CADDetector:
        return CADDetector(**vars(self).copy())


class RobustDetectorBuilder(BaseBuilder):

    def __init__(self, window=100, threshold=0.9999):
        self.window = window
        self.threshold = threshold

    def set_window(self, window):
        self.window = window
        return self

    def set_threshold(self, threshold):
        self.threshold = threshold
        return self

    def build(self) -> RobustDetector:
        return RobustDetector(**vars(self).copy())


class EngineBuilderFactory(object):

    engines = OrderedDict(
        [
            ("robust", {
                "key": "robust",
                "name": "RobustDetector"
            }),
            ("cad", {
                "key": "cad",
                "name": "CADDetector"
            }),
        ]
    )

    @staticmethod
    def get_robust():
        return RobustDetectorBuilder()

    @staticmethod
    def get_cad():
        return CADDetectorBuilder()
