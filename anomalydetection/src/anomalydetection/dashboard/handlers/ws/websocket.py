# -*- coding: utf-8 -*-

from tornado.websocket import WebSocketHandler

web_sockets = []


class WebSocket(WebSocketHandler):

    kafka_sink = None
    kafka_producer = None
    kafka_files_topic = None
    kafka_images_topic = None

    def initialize(self):
        global web_sockets, kafka_sink
        super(WebSocket, self).initialize()

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        global web_sockets
        if self not in web_sockets:
            web_sockets.append(self)

    def on_close(self):
        global web_sockets
        if self in web_sockets:
            web_sockets.remove(self)
            del self

    def data_received(self, chunk):
        pass

    def on_message(self, message):
        pass
