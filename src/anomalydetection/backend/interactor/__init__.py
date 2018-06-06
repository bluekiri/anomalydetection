# -*- coding: utf-8 -*- #

from anomalydetection.backend.engine.builder import BaseBuilder
from anomalydetection.backend.entities import BaseMessageHandler
from anomalydetection.backend.stream import BaseObservable


class BaseWarmUp(BaseObservable):
    pass


class BaseEngineInteractor(object):

    def __init__(self,
                 engine_builder: BaseBuilder,
                 message_handler: BaseMessageHandler) -> None:
        super().__init__()
        self.engine_builder = engine_builder
        self.message_handler = message_handler
        self.app_engine = {}

    def get_engine(self, application: str):
        if application not in self.app_engine:
            self.app_engine[application] = self.engine_builder.build()
        return self.app_engine[application]
