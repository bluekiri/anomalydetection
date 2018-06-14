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

from tornado.escape import json_encode

from anomalydetection.dashboard.handlers.base import BaseHandler


class BaseJSONHandler(BaseHandler):
    """
    Abstract Handler for HTML responses, this will render a json document
    """

    content_type = "application/json"

    def data_received(self, chunk):
        pass

    async def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', self.content_type)

        # in debug mode, add traceback
        trace = []
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            for line in traceback.format_exception(*kwargs["exc_info"]):
                trace.append(line)

        self.finish(json_encode({
            'error': {
                'code': status_code,
                'message': self._reason,
                'traceback': trace,
            }
        }))

    def response(self, code, chunk):
        self.set_status(code)
        self.write(json_encode(chunk))

    def error(self, status_code, reason):
        self.set_status(status_code, reason)
        self.write_error(self.get_status())
