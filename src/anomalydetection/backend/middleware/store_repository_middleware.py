# -*- coding:utf-8 -*-
import logging

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.middleware import Middleware


class StoreRepositoryMiddleware(Middleware):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, repository: BaseRepository) -> None:
        super().__init__()
        self.repository = repository
        self.repository.initialize()

    def on_next(self, value):
        self.repository.insert(value)

    def on_error(self, error):
        self.logger.error(error)

    def on_completed(self):
        self.logger.info("Completed!")
