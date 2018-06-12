# -*- coding: utf-8 -*-

from tornado import web

from anomalydetection.dashboard.handlers.base.json \
    import BaseJSONHandler
from anomalydetection.dashboard.handlers.base.html \
    import AuthMixin


class SecureJSONHandler(BaseJSONHandler, AuthMixin):

    @web.authenticated
    def response(self, code, chunk):
        super(SecureJSONHandler, self).response(code, chunk)
