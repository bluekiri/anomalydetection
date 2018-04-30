# -*- coding: utf-8 -*-

import os

from anomalydetection.dashboard.conf import config

# Settings
from anomalydetection.dashboard.lib import ui

print(os.path.join(os.path.realpath(os.curdir)))
settings = {
    'debug': True,  # Debug
    'autoreload': True,  # Auto reload on file changes, depends on debug = True
    'static_path': os.path.join(os.path.realpath(os.curdir), "static"),
    'template_path': os.path.join(os.path.realpath(os.curdir), "templates"),
    'ui_modules': ui,
    'conf': config,
    # Hardcoded cookie_secret allows to keep session while developing
    'cookie_secret': '504186dd-b516-4fb0-bcae-7592717e3dc3',
    'login_url': "/login"
}
