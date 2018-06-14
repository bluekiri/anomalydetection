# -*- coding: utf-8 -*- #
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
