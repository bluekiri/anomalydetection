# -*- coding:utf-8 -*- #
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
#

import os

TEST_PATH = os.path.realpath(os.path.dirname(__file__))

config = {
    "KAFKA_BROKER": os.getenv("KAFKA_BROKER", "localhost:9092"),
    "SQLITE_DATABASE_FILE": os.getenv("SQLITE_DATABASE_FILE", "/tmp/database.sqlite"),
}

os.environ["SQLITE_DATABASE_FILE"] = config["SQLITE_DATABASE_FILE"]
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
os.environ["PUBSUB_PROJECT_ID"] = "testing"
os.environ["ASYNC_TEST_TIMEOUT"] = "100"
