# -*- coding: utf-8 -*-

from time import mktime
from datetime import datetime


def timestamp(date, format="%Y-%m-%d"):
    return int(mktime(datetime.strptime(date, format).timetuple()) * 1000)
