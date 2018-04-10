# -*- coding:utf-8 -*- #


class BaseEngine(object):

    def predict(self, value: float) -> float:
        raise NotImplementedError("To implement in child classes.")
