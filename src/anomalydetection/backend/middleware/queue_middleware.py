# -*- coding:utf-8 -*- #
import asyncio
import json

import websockets

from anomalydetection.backend.middleware import Middleware


class WebSocketDashboardMiddleware(Middleware):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def on_next(self, value):

        # Create an event loop
        asyncio.set_event_loop(asyncio.new_event_loop())

        async def ws_send(item):
            async with websockets.connect('ws://localhost:5000/ws/') as ws:
                item_dict = item.to_dict(True)
                item_dict.update({"signal": self.name})
                await ws.send(json.dumps(item_dict))

        # Run with asyncio
        asyncio.get_event_loop().run_until_complete(ws_send(value))

    def on_error(self, error):
        pass

    def on_completed(self):
        pass
