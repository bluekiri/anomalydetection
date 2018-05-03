# -*- coding: utf-8 -*-

from anomalydetection.dashboard.handlers.base.html import SecureHTMLHandler
from anomalydetection.dashboard.handlers.base.helpers.error import Error


class NotFound(SecureHTMLHandler):

    error_template = "404.html"

    async def get(self, *args, **kwargs):
        self.print_error(error=Error(404, "Error Page"))
