# -*- coding: utf-8 -*-

from anomalydetection.dashboard.lib.handlers.html.base_html import BaseHTMLHandler
from anomalydetection.dashboard.lib.handlers.html.auth import AuthMixin


class SecureHTMLHandler(BaseHTMLHandler, AuthMixin):

    def response(self, **kwargs):
        maintenance = False
        if maintenance:
            self.redirect("/maintenance/")
        else:
            self.set_status(self.default_response_code)
            self.render(self.template, **kwargs)

    def render(self, template_name, **kwargs):
        return super(SecureHTMLHandler, self).render(template_name,
                                                     username=self.get_display_name(),
                                                     **kwargs)
