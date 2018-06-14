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
from anomalydetection.backend.engine.base_engine import BaseEngine
from anomalydetection.backend.entities.output_message import AnomalyResult
from statsmodels.robust.scale import mad


class RobustDetector(BaseEngine):
    """
    Anomaly detection engine based in robust statistics:
    median and median absolute deviation.
    """

    def __init__(self, window=100, threshold=0.9999):
        """Default values to be determined for the anomaly detection"""
        self._data = np.full((window, 1), fill_value=np.nan)
        self._median = None
        self._mad = None
        self.threshold = threshold

    def _update_buffer(self, value):
        """Updates the buffered data with the new event.

        Appends the event at the end of self._data and clears the first
        registry in a FIFO fashion.
        Keeps the size of self._data constant.

        Parameters
        ----------
        value: float
            Value to be included in the last position of buffer.
        """
        self._data[:-1] = self._data[1:]
        self._data[-1] = value

    def _update_statistics(self):
        """Updates the robust statistics based in the buffered data.
        """
        self._median = np.median(self._data)
        self._mad = mad(self._data)[0]

    def _update(self, value):
        """Updates the buffered data with the new event and the robust statistics.

        Appends the event at the end of self._data and clears the first
        registry in a FIFO fashion.
        Once the buffer is updated, updates the median and mad

        Parameters
        ----------
        value: float
            Value to be included in the last position of buffer.
        """
        self._update_buffer(value=value)
        self._update_statistics()

    def predict(self, value, **kwargs) -> AnomalyResult:
        """
        Return the probability of being an outlier

        Calculates the probability of value being an anomaly with respect past events.
        Once it has been computed, the buffer data is updated and the statistic parameters
        recalculated.

        Parameters
        ----------
        value: float
            Value to be included in the last position of buffer.

        Returns
        ------
        results: dict
            results['anomaly_probability']: Probability that the value is an
                                            anomaly given the last observations.
            results['is_anomaly']: Boolean indicator. 1 if it is an anomaly
                                   based on threshold else 0.
            results['value_upper_limit']: Value upper limit.
            results['value_lower_limit']: Value lower limit.
        """
        results = {}
        if np.isnan(self._data).any():
            results['anomaly_probability'] = -1
            results['is_anomaly'] = -1
            results['value_upper_limit'] = -1
            results['value_lower_limit'] = -1
        else:
            z_score = np.abs(value - self._median) / self._mad
            results['anomaly_probability'] = 1 - st.norm.sf(z_score)
            results['is_anomaly'] = int(results['anomaly_probability'] >= self.threshold)
            results['value_upper_limit'] = \
                (self._median + self._mad*st.norm.ppf(self.threshold))
            results['value_lower_limit'] = \
                (self._median - self._mad*st.norm.ppf(self.threshold))
        self._update(value=value)

        return AnomalyResult(**results)
