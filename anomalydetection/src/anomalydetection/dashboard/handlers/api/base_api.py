# -*- coding: utf-8 -*-

from anomalydetection.dashboard.lib.handlers.json.base_json import BaseJSONHandler
from anomalydetection.dashboard.lib.handlers.json.secure_json import SecureJSONHandler


class UnsecureHandler(BaseJSONHandler):
    pass


class SecuredHandler(UnsecureHandler, SecureJSONHandler):
    pass
