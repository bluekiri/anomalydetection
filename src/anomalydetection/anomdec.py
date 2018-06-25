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
import sys
from time import sleep

from anomalydetection.backend.backend import main as backend_main
from anomalydetection.common.config import Config
from anomalydetection.common.logging import LoggingMixin
from anomalydetection.dashboard.dashboard import main as dashboard_main

__root__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(__root__)


class Anomdec(LoggingMixin):

    def run(self):
        self.logger.info("Starting anomdec")
        try:
            if sys.argv[1] == "dashboard":
                self.logger.info("Run dashboard")
                dashboard_main([], Config())
            elif sys.argv[1] == "backend":
                self.logger.info("Run backend")
                backend_main(Config())
            elif sys.argv[1] == "devel":

                from anomalydetection.backend.devel_mode import produce_messages

                # Prepare settings for devel mode
                os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
                os.environ["PUBSUB_PROJECT_ID"] = "testing"
                os.environ["ASYNC_TEST_TIMEOUT"] = "100"

                self.logger.info("Creating configuration")
                config = Config("devel")
                sleep(5)

                self.logger.info("Run dashboard, backend and producer")
                dashboard_main([backend_main, produce_messages], config)

        except IndexError as _:
            self.logger.info("Run dashboard and backend")
            dashboard_main([backend_main])


if __name__ == '__main__':
    Anomdec().run()
