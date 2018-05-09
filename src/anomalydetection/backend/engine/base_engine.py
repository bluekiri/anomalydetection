# -*- coding:utf-8 -*- #


class BaseEngine(object):

    def predict(self, value: float, **kwargs) -> float:
        raise NotImplementedError("To implement in child classes.")
