# -*- coding: utf-8 -*-

from tornado import web

from anomalydetection.dashboard.lib.handlers.json.base_json import BaseJSONHandler
from anomalydetection.dashboard.lib.handlers.html.auth import AuthMixin


class SecureJSONHandler(BaseJSONHandler, AuthMixin):

    @web.authenticated
    def response(self, code, chunk):
        super(SecureJSONHandler, self).response(code, chunk)

