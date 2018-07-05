# -*- coding:utf-8 -*- #
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

import numpy as np
import scipy.stats as st

from anomalydetection.common.logging import LoggingMixin
from anomalydetection.backend.engine import BaseEngine
from anomalydetection.backend.entities.output_message import AnomalyResult
from statsmodels.robust.scale import mad


class RobustDetector(BaseEngine, LoggingMixin):

    def __init__(self, window=100, threshold=0.9999) -> None:
        """
        Anomaly detection engine based in robust statistics,
        median and median absolute deviation.

        :param window:     window of samples to work with
        :param threshold:  threshold for confidence
        """
        self._data = np.full((window, 1), fill_value=np.nan)
        self._median = np.nan
        self._mad = np.nan
        self.threshold = threshold

    def _update_buffer(self, value):
        self._data[:-1] = self._data[1:]
        self._data[-1] = value

    def _update_statistics(self):
        if not np.isnan(self._data).any():
            self._median = np.median(self._data)
            self._mad = mad(self._data)[0]

    def _update(self, value):
        self._update_buffer(value=value)
        self._update_statistics()

    def predict(self, value: float, **kwargs) -> AnomalyResult:
        results = {}
        if np.isnan(self._data).any():
            results['anomaly_probability'] = -1
            results['is_anomaly'] = -1
            results['value_upper_limit'] = -1
            results['value_lower_limit'] = -1
        else:
            if self._mad != 0:
                z_score = np.abs(value - self._median) / self._mad
            else:
                z_score = np.inf
            results['anomaly_probability'] = 1 - st.norm.sf(z_score)
            results['is_anomaly'] = int(results['anomaly_probability'] >= self.threshold)
            results['value_upper_limit'] = \
                (self._median + self._mad*st.norm.ppf(self.threshold))
            results['value_lower_limit'] = \
                (self._median - self._mad*st.norm.ppf(self.threshold))
        self._update(value=value)

        return AnomalyResult(**results)
