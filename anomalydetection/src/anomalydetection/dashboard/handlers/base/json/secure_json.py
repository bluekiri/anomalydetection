# -*- coding: utf-8 -*-

from tornado import web

from dashboard.handlers.base.json.base_json \
    import BaseJSONHandler
from dashboard.handlers.base.html \
    import AuthMixin


class SecureJSONHandler(BaseJSONHandler, AuthMixin):

    @web.authenticated
    def response(self, code, chunk):
        super(SecureJSONHandler, self).response(code, chunk)

