"""
This module provides functions for calculating harmonic sums using different summation methods.

Authors: M. van Straten, P. Merz

Usage Examples:
---------------

Example usage of `harmonic_sum`:

    # Calculate harmonic sums using Kahan summation method
    print(harmonic_sum(10, kahan_sum, np.float32))
    
    # Calculate harmonic sums using forward summation method
    print(harmonic_sum(5, forward_sum, np.float32))
"""

from functools import partial, reduce

import numpy as np

from ewr_so_se_2024.py_logspace import py_logspace


def forward_sum(n: int, dtype=np.float32):
    """
    Calculates the n-th harmonic sum using forward summation method.

    Args:
        n: Number of terms in the harmonic sum.
        dtype: Data type of the summands. Default is np.float32.

    Returns:
        The n-th harmonic sum.
    """
    return reduce(
        lambda partial_sum, n: partial_sum + dtype(1) / dtype(n),
        range(1, n + 1),
        dtype(0),
    )


def kahan_sum(n: int, dtype=np.float32):
    """
    Calculates the n-th harmonic sum using Kahan summation method.

    Args:
        n: Number of terms in the harmonic sum.
        dtype: Data type of the summands.

    Returns:
        The n-th harmonic sum.
    """
    sum = dtype(0)
    # Correction term
    c = dtype(0)
    for k in range(1, n + 1):
        y = dtype(1) / dtype(k) - c
        t = sum + y
        c = (t - sum) - y
        sum = t
    return sum


def harmonic_sum(n: int, method, dtype=np.float32):
    """
    Determines the summation method for calculating the n-th harmonic sum.

    Args:
        n: The number of logarithmically spaced terms to sample the harmonic series at.
        method: The summation method to be used.
        dtype: Data type of the summands.

    Returns:
        List of harmonic sums calculated using the specified method.
    """
    return list(map(partial(method, dtype=dtype), py_logspace(1, 5, n)))


def main():
    """
    Main function to demonstrate the usage of `harmonic_sum` with different summation methods.
    """
    print(harmonic_sum(10, kahan_sum, np.float32))
    print(harmonic_sum(5, forward_sum, np.float32))


if __name__ == "__main__":
    main()
