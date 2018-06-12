# -*- coding: utf-8 -*-

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
