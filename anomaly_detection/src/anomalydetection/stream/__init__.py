# -*- coding:utf-8 -*-


class StreamBackend(object):

    def poll(self) -> str:
        raise NotImplementedError("To implement in child classes.")

    def push(self, message: str):
        raise NotImplementedError("To implement in child classes.")