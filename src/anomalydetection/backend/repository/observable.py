# -*- coding:utf-8 -*- #
import datetime

from rx import Observable

from anomalydetection.backend.repository import BaseRepository
from anomalydetection.backend.repository import BaseObservableRepository


class ObservableRepository(BaseObservableRepository):

    def __init__(self, repository: BaseRepository,
                 application=None, from_ts=None, to_ts=None) -> None:
        super().__init__(repository)
        self.application = application
        self.from_ts = from_ts
        self.to_ts = to_ts

        if not self.to_ts:
            self.to_ts = datetime.datetime.now()
        if not self.from_ts:
            self.from_ts = self.to_ts - datetime.timedelta(hours=24)

    def _get_observable(self):
        return Observable.from_(self.repository.fetch(self.application,
                                                      self.from_ts,
                                                      self.to_ts))
