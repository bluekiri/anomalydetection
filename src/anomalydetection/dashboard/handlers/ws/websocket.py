# -*- coding: utf-8 -*-
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

from tornado.websocket import WebSocketHandler


class WebSocket(WebSocketHandler):

    web_sockets = []

    def initialize(self):
        super(WebSocket, self).initialize()

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        if self not in WebSocket.web_sockets:
            WebSocket.web_sockets.append(self)

    def on_close(self):
        if self in WebSocket.web_sockets:
            WebSocket.web_sockets.remove(self)
            del self

    def data_received(self, chunk):
        pass

    def on_message(self, message):
        for ws in WebSocket.web_sockets:
            if ws != self:
                ws.write_message(message)
