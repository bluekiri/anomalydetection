# -*- coding: utf-8 -*-

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
