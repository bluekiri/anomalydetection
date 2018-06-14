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

from tornado import web

from anomalydetection.dashboard.handlers.base.html \
    import BaseHTMLHandler
from anomalydetection.dashboard.handlers.base.html \
    import SecureHTMLHandler


class Home(SecureHTMLHandler):

    template = "home.html"

    @web.asynchronous
    async def get(self):
        self.response()


class Maintenance(BaseHTMLHandler):
    template = "maintenance.html"

    async def get(self):
        self.response(h_title="Maintenance")


class MaintenanceSwitch(SecureHTMLHandler):
    template = "maintenance.html"

    async def get(self):
        raise NotImplemented

    async def switch_maintenance(self, status):
        return status


class MaintenanceEnable(MaintenanceSwitch):

    async def get(self):
        res = await self.switch_maintenance(True)
        if res:
            self.response(h_title="Maintenance enabled")


class MaintenanceDisable(MaintenanceSwitch):

    async def get(self):
        res = await self.switch_maintenance(False)
        if res:
            self.response(h_title="Maintenance enabled")
