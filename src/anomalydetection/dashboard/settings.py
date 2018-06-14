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

import os
import uuid

from anomalydetection.dashboard.handlers.base import ui

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_RANDOM_COOKIE_SECRET = str(uuid.uuid4())

settings = {
    'debug': False,  # Debug
    'autoreload': False,  # Auto reload on file changes, depends on debug = True
    'static_path': os.path.join(BASE_PATH, "static"),
    'template_path': os.path.join(BASE_PATH, "templates"),
    'ui_modules': ui,
    'cookie_secret': os.getenv("COOKIE_SECRET", DEFAULT_RANDOM_COOKIE_SECRET),
    'login_url': "/login"
}
