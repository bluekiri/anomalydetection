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

import asyncio
import json

import websockets

from anomalydetection.backend.sink import BaseSink
from anomalydetection.common.logging import LoggingMixin


class WebSocketSink(BaseSink, LoggingMixin):

    def __init__(self, name: str, url: str) -> None:
        """
        Implementation to Sink OutputMessage stream to a WebSocket

        :param name:   name
        :param url:    websocket url
        """
        super().__init__()
        self.name = name
        self.url = url

    def on_next(self, value):

        # Create an event loop
        asyncio.set_event_loop(asyncio.new_event_loop())

        async def ws_send(item):
            async with websockets.connect(self.url) as ws:
                item_dict = item.to_dict(True)
                item_dict.update({"signal": self.name})
                self.logger.debug(
                    "Sending message to Websocket: {}".format(
                        json.dumps(item_dict)))
                await ws.send(json.dumps(item_dict))

        # Run with asyncio
        asyncio.get_event_loop().run_until_complete(ws_send(value))

    def on_error(self, error):
        pass

    def on_completed(self):
        pass
