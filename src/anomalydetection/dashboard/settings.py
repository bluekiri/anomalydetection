# -*- coding: utf-8 -*-

import os

from anomalydetection.dashboard.conf import config
from anomalydetection.dashboard.handlers.base import ui

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_COOKIE_SECRET = '504186dd-b516-4fb0-bcae-7592717e3dc3'

settings = {
    'debug': False,  # Debug
    'autoreload': False,  # Auto reload on file changes, depends on debug = True
    'static_path': os.path.join(BASE_PATH, "static"),
    'template_path': os.path.join(BASE_PATH, "templates"),
    'ui_modules': ui,
    'conf': config,
    # Hardcoded cookie_secret allows to keep session while developing
    'cookie_secret': os.getenv("COOKIE_SECRET", DEFAULT_COOKIE_SECRET),
    'login_url': "/login"
}
