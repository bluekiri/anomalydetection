# -*- coding:utf-8 -*- #

import numpy as np


def sum(values):
    return np.sum(np.array(values))


def avg(values):
    return np.average(np.array(values))


def p50(values):
    np.percentile(np.array(values), 95)


def p75(values):
    np.percentile(np.array(values), 75)


def p95(values):
    np.percentile(np.array(values), 95)


def p99(values):
    np.percentile(np.array(values), 99)
