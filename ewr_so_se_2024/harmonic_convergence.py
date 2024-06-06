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

from functools import reduce
from itertools import accumulate, chain, islice, pairwise
from typing import Any, cast, TypeVar

import numpy as np

from ewr_so_se_2024.py_logspace import py_logspace


# Type hint for type checking (only used for static type checkers)
T = TypeVar("T", bound=np.floating[Any])


def vectorized_sum(
    partial_sum: T,
    start: int,
    stop: int,
    dtype: type[T] = np.float32,
) -> T:
    """
    Calculates the n-th harmonic sum using vectorization.

    Args:
        n: Number of terms in the harmonic sum.
        dtype: Data type of the summands. Default is np.float32.

    Returns:
        The n-th harmonic sum.
    """
    return cast(
        T,
        np.sum(
            np.concatenate(
                ([partial_sum], dtype(1) / np.arange(start + 1, stop + 1, dtype=dtype))
            )
        ),
    )


def forward_sum(
    partial_sum: T,
    start: int,
    stop: int,
    dtype: type[T] = np.float32,
) -> T:
    """
    Calculates the n-th harmonic sum using forward summation method.

    Args:
        n: Number of terms in the harmonic sum.
        dtype: Data type of the summands. Default is np.float32.

    Returns:
        The n-th harmonic sum.
    """
    return cast(
        T,
        reduce(
            lambda partial_sum, n: partial_sum + dtype(1) / dtype(n),
            range(start + 1, stop + 1),
            partial_sum,
        ),
    )


def kahan_sum(partial_sum: T, start: int, stop: int, dtype: type[T] = np.float32) -> T:
    """
    Calculates the n-th harmonic sum using Kahan summation method.

    Args:
        n: Number of terms in the harmonic sum.
        dtype: Data type of the summands.

    Returns:
        The n-th harmonic sum.
    """
    correction_term = dtype(0)
    for k in range(start + 1, stop + 1):
        y = dtype(1) / dtype(k) - correction_term
        t = cast(T, partial_sum + y)
        correction_term = (t - partial_sum) - y
        partial_sum = t
    return partial_sum


# pylint: disable=too-many-arguments
def harmonic_sum(
    logspace_start,
    logspace_stop,
    logspace_basis,
    n: int,
    summation_algorithm,
    dtype: type[T] = np.float32,
) -> list[T]:
    """
    Determines the summation method for calculating the n-th harmonic sum.

    Args:
        n: The number of logarithmically spaced terms to sample the harmonic series at.
        method: The summation method to be used.
        dtype: Data type of the summands.

    Returns:
        List of harmonic sums calculated using the specified method.
    """
    return list(
        islice(
            accumulate(
                pairwise(
                    chain(
                        [0],
                        py_logspace(logspace_start, logspace_stop, n, logspace_basis),
                    )
                ),
                lambda partial_sum, start_stop: summation_algorithm(
                    partial_sum, *start_stop, dtype=dtype
                ),
                initial=dtype(0),
            ),
            1,
            None,
        )
    )


def main():
    """
    Main function to demonstrate the usage of `harmonic_sum` with different summation methods.
    """
    kahan_results = harmonic_sum(0, 5, 10, 10, kahan_sum, np.float32)
    forward_results = harmonic_sum(0, 5, 10, 10, forward_sum, np.float32)

    print(
        "Harmonic sums using Kahan summation method (logarithmic spacing from 1 to 100000):"
    )
    print(kahan_results)

    print(
        "\nHarmonic sums using forward summation method (logarithmic spacing from 1 to 100000):"
    )
    print(forward_results)


if __name__ == "__main__":
    main()
