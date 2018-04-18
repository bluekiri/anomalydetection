# -*- coding:utf-8 -*-
from anomalydetection.backend.store_middleware import Middleware


class SqliteStoreToMiddleware(Middleware):

    def __init__(self, filename: str, logger) -> None:
        super().__init__()
        self.logger = logger
        self.filename = filename

    def on_next(self, value):
        file = open(self.filename, "a")
        file.write(str(value) + "\n")
        file.close()

    def on_error(self, error):
        self.logger.error(error)

    def on_completed(self):
        self.logger.info("Completed!")
