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

from threading import Lock

from anomalydetection.backend.engine.builder import BaseEngineBuilder
from anomalydetection.backend.entities import BaseMessageHandler


class BaseEngineInteractor(object):

    """
    BaseEngineInteractor is responsible to hold the engine builder
    and the message handler. It's also responsible for build engines
    for each application
    """

    def __init__(self,
                 engine_builder: BaseEngineBuilder,
                 message_handler: BaseMessageHandler) -> None:
        """
        BaseEngineInteractor constructor

        :param engine_builder:    engine builder
        :param message_handler:   message handler
        """
        super().__init__()
        self.engine_builder = engine_builder
        self.message_handler = message_handler
        self.app_engine = {}
        self.lock = Lock()

    def get_engine(self, application: str):
        """
        Return the engine for the application in a thread safe way

        :param application:   application name
        :return:              its engine
        """
        if application not in self.app_engine:
            with self.lock:
                if application not in self.app_engine:
                    self.app_engine[application] = self.engine_builder.build()
        return self.app_engine[application]
