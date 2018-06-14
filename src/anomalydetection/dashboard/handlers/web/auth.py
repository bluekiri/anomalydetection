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


class AuthResponse:

    def __init__(self,
                 auth: bool,
                 display_name: str = "anonymous",
                 error: str = "",
                 maintenance: bool=False):
        self.auth = auth
        self.display_name = display_name
        self.error_cause = error
        self.maintenance = maintenance


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
            self.set_secure_cookie("user", auth_res.display_name)
            self.redirect(self.get_argument("next"))
        else:
            self.response(title="Login", error=auth_res.error_cause)

    async def auth(self) -> AuthResponse:

        # TODO: Create a true auth
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username and password and None:
            return AuthResponse(False, error="Not implemented")
        return AuthResponse(False, error="Invalid username or password.")


class Logout(BaseHTMLHandler):

    async def get(self):
        self.clear_all_cookies()
        self.redirect("/")
