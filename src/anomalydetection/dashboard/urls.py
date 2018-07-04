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

from anomalydetection.dashboard.handlers.web.auth import Login, Logout
from anomalydetection.dashboard.handlers.web.main import Home
from anomalydetection.dashboard.handlers.web.main import Maintenance
from anomalydetection.dashboard.handlers.web.main import MaintenanceEnable
from anomalydetection.dashboard.handlers.web.main import MaintenanceDisable
from anomalydetection.dashboard.handlers.web.signal import SignalList
from anomalydetection.dashboard.handlers.web.signal import SignalDetail
from anomalydetection.dashboard.handlers.web.signal import SignalData
from anomalydetection.dashboard.handlers.web.signal import SignalSandbox
from anomalydetection.dashboard.handlers.ws.websocket import WebSocket

from anomalydetection.dashboard.handlers.web.errors import NotFound

urls = [
    (r'/?', Home),
    (r'/signals/?', SignalList),
    (r'/signals/sandbox/?', SignalSandbox),
    (r'/signals/([^/]*)/?', SignalDetail),
    (r'/signals/([^/]*)/data/?', SignalData),
    (r'/maintenance/disable/?', MaintenanceDisable),
    (r'/maintenance/enable/?', MaintenanceEnable),
    (r'/maintenance/?', Maintenance),
    (r'/login/?', Login),
    (r'/logout/?', Logout),
    (r'/ws/?', WebSocket),
    (r'.*', NotFound)
]
