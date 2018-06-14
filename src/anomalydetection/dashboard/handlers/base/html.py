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

import traceback

from tornado import web
from tornado.web import RequestHandler

from anomalydetection.dashboard.handlers.base.helpers.error import Error
from anomalydetection.dashboard.handlers.base import BaseHandler


class BaseHTMLHandler(BaseHandler):
    """
    Abstract Handler for HTML responses, this will render a template with some data, this
    class should be extended defining template, title, get, post, push, etc... methods
    """

    db = None
    template = None
    error_template = "500.html"
    maintenance = False

    def data_received(self, chunk):
        pass

    def write_error(self, status_code, **kwargs):
        """
        Write an error in HTML format.
        :param status_code:  The status code, 4xx or 5xx.
        :param kwargs:       A Keyword argument list.
        :return:             Prints an error.
        """
        self.set_header('Content-Type', 'text/html')

        # in debug mode, add traceback
        trace = []
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            for line in traceback.format_exception(*kwargs["exc_info"]):
                trace.append(line.strip())

        # Error object
        error = Error(status_code, self._reason, trace)

        # Print it
        self.print_error(error)

    def response(self, **kwargs):
        self.set_status(self.default_response_code)
        self.render(self.template, **kwargs)

    def print_error(self, error):
        self.set_status(error.code, error.message)
        self.render(self.error_template, error=error)


class AuthMixin(RequestHandler):

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("session")

    def get_display_name(self):
        return self.get_secure_cookie("user")


class SecureHTMLHandler(BaseHTMLHandler, AuthMixin):

    def response(self, **kwargs):
        maintenance = False
        if maintenance:
            self.redirect("/maintenance/")
        else:
            self.set_status(self.default_response_code)
            self.render(self.template, **kwargs)

    @web.authenticated
    def render(self, template_name, **kwargs):
        return super(SecureHTMLHandler,
                     self).render(template_name,
                                  username=self.get_display_name(),
                                  **kwargs)


class ErrorHandler(SecureHTMLHandler):
    pass
