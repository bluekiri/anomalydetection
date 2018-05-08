# -*- coding:utf-8 -*- #
import json
from collections import OrderedDict

from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.engine.robust_z_engine import RobustDetector


class EngineFactory(object):

    engines = OrderedDict(
        [
            ("robust", {
                "key": "robust",
                "name": "RobustDetector"
            })
        ]
    )

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs

    def get(self) -> BaseEngine:
        try:
            if self.kwargs["engine"] == "robust":
                return self.get_robust()
        except Exception as ex:
            raise ex
            raise RuntimeError(
                "Cannot instantiate the engine with this params {}"
                .format(json.dumps(self.kwargs)))

    def get_robust(self):
        return RobustDetector(window=int(self.kwargs["window"]),
                              threshold=float(self.kwargs["threshold"]))
