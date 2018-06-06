# -*- coding:utf-8 -*- #

from enum import Enum


class AggregationFunction(Enum):

    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    P50 = "percentile50"
    P75 = "percentile75"
    P95 = "percentile95"
    P99 = "percentile99"
