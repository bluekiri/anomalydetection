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

import logging
import logging.config
import os

import yaml


class LoggingMixin(object):

    __logger_configured = False

    @property
    def logger(self):
        """
        Logger object.

        :return:  a configured logger object
        """
        name = '.'.join([self.__class__.__module__,
                         self.__class__.__name__])\
            .replace("__main__", "anomalydetection")
        root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        if not self.__logger_configured:
            logging_conf = os.environ["HOME"] + "/anomdec/logging.yml"
            if not os.path.exists(logging_conf):
                logging_conf = root + '/logging.yml'
            with open(logging_conf, 'rt') as f:
                config = yaml.load(f.read())
                logging.config.dictConfig(config)
            self.__logger_configured = True

        return logging.getLogger(name)
