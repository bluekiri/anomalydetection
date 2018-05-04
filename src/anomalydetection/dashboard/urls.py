# -*- coding: utf-8 -*-

from anomalydetection.dashboard.handlers.web.auth import Login, Logout
from anomalydetection.dashboard.handlers.web.main import Home
from anomalydetection.dashboard.handlers.web.main import Maintenance
from anomalydetection.dashboard.handlers.web.main import MaintenanceEnable
from anomalydetection.dashboard.handlers.web.main import MaintenanceDisable
from anomalydetection.dashboard.handlers.ws.websocket import WebSocket

from anomalydetection.dashboard.handlers.web.errors import NotFound

urls = [
    (r'/?', Home),
    (r'/maintenance/disable/?', MaintenanceDisable),
    (r'/maintenance/enable/?', MaintenanceEnable),
    (r'/maintenance/?', Maintenance),
    (r'/login/?', Login),
    (r'/logout/?', Logout),
    (r'/ws/?', WebSocket),
    (r'.*', NotFound)
]
