# -*- coding:utf-8 -*- #

from collections import OrderedDict

from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.engine.cad_engine import CADDetector
from anomalydetection.backend.engine.robust_z_engine import RobustDetector


class EngineFactory(object):

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

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs

    def get(self) -> BaseEngine:
        try:
            if self.kwargs["engine"] == "robust":
                return self.get_robust()
            if self.kwargs["engine"] == "cad":
                return self.get_cad()
        except Exception as ex:
            raise ex

    def get_robust(self):
        return RobustDetector(window=int(self.kwargs["window"]),
                              threshold=float(self.kwargs["threshold"]))

    def get_cad(self):
        return CADDetector(min_value=float(self.kwargs["min_value"]),
                           max_value=float(self.kwargs["max_value"]),
                           threshold=float(self.kwargs["threshold"]))
