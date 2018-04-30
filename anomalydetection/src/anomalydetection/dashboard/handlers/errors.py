# -*- coding: utf-8 -*-

from anomalydetection.dashboard.lib.handlers.html.secure_html import SecureHTMLHandler
from anomalydetection.dashboard.lib.helpers.error import Error


class NotFound(SecureHTMLHandler):

    error_template = "404.html"

    async def get(self, *args, **kwargs):
        self.print_error(error=Error(404, "Error Page"))
