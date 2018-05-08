# -*- coding: utf-8 -*-


class Error:

    code = None
    message = ""
    backtrace = []

    def __init__(self, cod, msg, bt=[]):
        """
        Error Constructor.
        :param cod: Error code.
        :param msg: Error message.
        :param bt:  Backtrace.
        """
        self.code = cod
        self.message = msg
        self.backtrace = bt
