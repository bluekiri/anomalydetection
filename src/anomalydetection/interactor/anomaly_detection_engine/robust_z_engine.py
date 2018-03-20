from anomalydetection.interactor.anomaly_detection_engine.base_engine import BaseEngine
import numpy as np
from statsmodels.robust.scale import mad
import math

class RobustDetector(BaseEngine):
    """Anomaly detection engine based in robust statistics: median and median absolute deviation
    """

    def __init__(self, window=100):
        """Default values to be determined for the anomaly detection"""
        self._data = np.full((window, 1), fill_value=np.nan)
        self._median = None
        self._mad = None

    def _update_buffer(self, value):
        """Updates the buffered data with the new event.

        Appends the event at the end of self._data and clears the first registry in a FIFO fashion.
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
        self._mad = mad(self._data)

    def _update(self, value):
        """Updates the buffered data with the new event and the robust statistics.

        Appends the event at the end of self._data and clears the first registry in a FIFO fashion.
        Once the buffer is updated, updates the median and mad

        Parameters
        ----------
        value: float
            Value to be included in the last position of buffer.
        """
        self._update_buffer(value=value)
        self._update_statistics()

    def predict(self, value):
        """
        Return the probability of being an outlier

        Parameters
        ----------
        value: float
            Value to be included in the last position of buffer.

        Returns
        ------
        anomaly_probability: float
            Probability that the value is an anomaly given the last observations.
        """
        if np.isnan(self._data).any():
            anomaly_probability = -1.
        else:
            z_score = np.abs(value - self._median) / self._mad
            anomaly_probability = 1 - 0.5 * math.erfc(z_score/math.sqrt(2))
        self._update(value=value)
        return anomaly_probability
