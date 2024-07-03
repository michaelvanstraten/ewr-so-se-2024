# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring


import numpy as np
from numpy import array, array_equal, logspace

from ewr_so_se_2024.harmonic_series.py_logspace import py_logspace


def test_numpy_compliance():
    assert array_equal(logspace(0, 3, num=5, dtype=int), py_logspace(0, 3))
    assert array_equal(
        logspace(0, 3, base=2, num=10, dtype=np.float_).round(12),
        array(py_logspace(0, 3, basis=2, num=10, dtype=np.float_)).round(12),
    )
    assert array_equal(
        logspace(0, 18, base=12, num=13, dtype=np.float_).round(12),
        array(py_logspace(0, 18, basis=12, num=13, dtype=np.float_)).round(12),
    )
    assert array_equal(
        logspace(0, 5, num=12, dtype=np.float32).round(12),
        array(py_logspace(0, 5, num=12, dtype=np.float32)).round(12),
    )
    assert array_equal(
        logspace(0, 20, num=23, dtype=np.float32).round(10),
        array(py_logspace(0, 20, num=23, dtype=np.float32)).round(10),
    )
