# -*- coding: utf-8 -*-
#
# Anomaly Detection Framework
# Copyright (C) 2018 Bluekiri BigData Team <bigdata@bluekiri.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime
import numpy as np

from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.entities.output_message import AnomalyResult


class EMADetector(BaseEngine):

    def __init__(self, window=100, threshold=2.0) -> None:
        """
        EMADetector constructor
        :param window:      window of samples to work with
        :param threshold:   threshold for confidence
        """
        super().__init__()
        self.window = window
        self.threshold = threshold
        self._std = np.nan
        self._ew_std = np.nan
        self._data = np.full((window, 4), fill_value=np.nan)

    def _extractor(self, **kwargs):
        if isinstance(kwargs["ts"], datetime):
            ts = kwargs["ts"]
            return [ts.weekday(), ts.hour, ts.minute]

    def _ema(self, data, window):
        weights = np.exp(np.linspace(-1., 1., window))
        weights /= weights.sum()
        ema = np.convolve(data[:, [0]][:, 0],
                          np.flip(weights, 0))
        return ema[len(data)-1:-len(data)+1]

    def _calc_std(self, data):
        return np.std(data[:, [0]][:, 0])

    def _update(self, value):
        self._update_buffer(value)
        self._update_statistics()

    def _update_buffer(self, value):
        self._data[:-1] = self._data[1:]
        self._data[-1] = value

    def _update_statistics(self):
        if not np.isnan(self._data).any():
            self._std = self._calc_std(self._data)

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        item = [value] + self._extractor(**kwargs)
        self._update_buffer(item)
        result = {}
        if np.isnan(self._data).any():
            result['anomaly_probability'] = -1
            result['is_anomaly'] = -1
            result['value_upper_limit'] = -1
            result['value_lower_limit'] = -1
        else:
            prediction = self._ema(self._data, self.window)[0]
            l_b = prediction - self._std * self.threshold
            u_b = prediction + self._std * self.threshold
            result['anomaly_probability'] = 0 if (u_b > value > l_b) else 1
            result['is_anomaly'] = False if (u_b > value > l_b) else True
            result['value_upper_limit'] = u_b
            result['value_lower_limit'] = l_b
        self._update(value=value)
        return AnomalyResult(**result.copy())
