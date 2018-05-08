# -*- coding: utf-8 -*-

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
        # FIXME: Create a true auth

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
