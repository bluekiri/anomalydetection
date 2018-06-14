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

import uuid

from anomalydetection.dashboard.handlers.base.html import BaseHTMLHandler


class Login(BaseHTMLHandler):

    template = "login.html"
    db = None

    async def get(self):
        maintenance = False
        if maintenance:
            self.redirect("/maintenance/")
        else:
            self.response(title="Login", error=False, udn=None)

    async def post(self):
        auth_res = await self.auth()
        if auth_res.maintenance:
            self.redirect("/maintenance/")
        if auth_res.auth:
            self.set_secure_cookie("session", str(uuid.uuid4()))
            display_name = " - ".join([auth_res.udn[0][1]["displayName"][0],
                                       auth_res.udn[0][1]["department"][0]])
            self.set_secure_cookie("user", display_name)
            self.redirect(self.get_argument("next"))
        else:
            self.response(title="Login", error=auth_res.error_cause)

    async def auth(self):
        # TODO: Create a true auth

        # Post arguments
        username = self.get_argument("username")
        password = self.get_argument("password")

        response = [
            [
                {},
                {
                    "displayName": [username],
                    "department": ["POCs"]
                }
            ]
        ]

        if username == "admin" and password == "admin":
            return AuthResponse(True, response)
        return AuthResponse(False, error="Invalid username or password.")


class Logout(BaseHTMLHandler):

    async def get(self):
        self.clear_all_cookies()
        self.redirect("/")


class AuthResponse:
    """
    AuthResponse class
    """

    auth = False
    error_cause = ""
    udn = None
    maintenance = False

    def __init__(self, au, udn=None, error="", maintenance=False):
        """
        Constructor for AuthResponse class
        :param au:     authentication result
        :param error:  error message (yes, shit happens)
        :param udn:    the udn
        """
        self.auth = au
        self.error_cause = error
        self.udn = udn
        self.maintenance = maintenance
