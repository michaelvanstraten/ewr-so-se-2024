""""""
from decimal import Decimal
from itertools import count, accumulate
import math
from typing import Callable, Iterable

from math import factorial, pi, sqrt

import random

PI = Decimal(pi)

RealValuedSequence = Iterable[Decimal]
Algoorithm = Callable[[], RealValuedSequence]


def leibniz():
    """"""
    return map(
        lambda item: 4 * item,
        accumulate(
            count(0),
            lambda partial_sum, n: partial_sum
            + ((-1) ** n) * Decimal(1) / Decimal(2 * n + 1),
            initial=0,
        ),
    )


class MonteCarlo(RealValuedSequence):
    """"""

    number_of_samples = 0
    samples_inside_of_unit_circle = 0

    def __iter__(self):
        return self

    def __next__(self) -> Decimal:
        random_x, random_y = random.random(), random.random()
        self.number_of_samples += 1
        if sqrt(random_x**2 + random_y**2) <= 1:
            self.samples_inside_of_unit_circle += 1
        return (
            4
            * Decimal(self.samples_inside_of_unit_circle)
            / Decimal(self.number_of_samples)
        )


def monte_carlo(seed: int = 69420) -> RealValuedSequence:
    """"""
    random.seed(seed)

    number_of_samples = 0
    samples_inside_of_unit_circle = 0

    while True:
        random_x, random_y = random.random(), random.random()
        number_of_samples += 1
        if sqrt(random_x**2 + random_y**2) <= 1:
            samples_inside_of_unit_circle += 1
        yield 4 * Decimal(samples_inside_of_unit_circle) / Decimal(number_of_samples)


def gauss_legendre():
    """"""
    a = Decimal(1)
    b = Decimal(1) / Decimal(2).sqrt()
    t = Decimal(1) / Decimal(4)
    p = Decimal(1)

    while True:
        next_a = (a + b) / 2
        b = (a * b).sqrt()
        t = t - p * (a - next_a) ** 2
        p = 2 * p
        a = next_a
        yield ((a + b) ** 2) / (4 * t)


def chudnovsky():
    """"""
    c = Decimal(426880) * Decimal(10005).sqrt()

    return map(
        lambda x: c * (1 / x),
        accumulate(
            count(1),
            lambda partial_sum, k: partial_sum
            + Decimal(math.factorial(6 * k) * (13591409 + 545140134 * k))
            / Decimal(factorial(3 * k) * factorial(k) ** 3 * (-640320) ** (3 * k)),
            initial=Decimal(13591409),
        ),
    )
