# -*- coding: utf-8 -*-

"""
File: funtions.py
Author: Cristòfol Torrens Morell <tofol.torrens@logitravel.com>
Description: Common used functions
"""

from time import mktime
from datetime import datetime


def timestamp(date, format="%Y-%m-%d"):
    return int(mktime(datetime.strptime(date, format).timetuple()) * 1000)
