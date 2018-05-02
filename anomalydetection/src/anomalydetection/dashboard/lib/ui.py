# -*- coding: utf-8 -*-

from tornado.web import UIModule


class UIError(UIModule):
    def render(self, error):
        return self.render_string("error.html", error=error)
