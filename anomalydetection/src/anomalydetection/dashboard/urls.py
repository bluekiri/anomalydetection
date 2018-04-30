# -*- coding: utf-8 -*-

from anomalydetection.dashboard.handlers.auth import Login, Logout
from anomalydetection.dashboard.handlers.main import Home
from anomalydetection.dashboard.handlers.main import Maintenance, MaintenanceEnable, MaintenanceDisable
from anomalydetection.dashboard.handlers.ws.websocket import WebSocket

from anomalydetection.dashboard.handlers.errors import NotFound

urls = [
    (r'/?', Home),
    (r'/maintenance/?', Maintenance),
    (r'/maintenance/enable/?', MaintenanceEnable),
    (r'/maintenance/disable/?', MaintenanceDisable),
    (r'/login/?', Login),
    (r'/logout/?', Logout),
    (r'/ws/?', WebSocket),
    (r'.*', NotFound)
]
