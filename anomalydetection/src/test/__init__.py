# -*- coding:utf-8 -*- #

import logging


class LoggingMixin(object):

    logger = logging.getLogger(__package__)
    logger.setLevel(logging.DEBUG)
