""""""
from collections import abc
from dataclasses import InitVar, dataclass
from decimal import Decimal
from math import factorial, sqrt


import random

RealValuedSequence = abc.Iterator[Decimal]


@dataclass
class ApproximationSequence(RealValuedSequence):
    current_position: int = -1

    def __iter__(self) -> Iterator[Decimal]:
        return self


@dataclass
class Leibniz(ApproximationSequence):
    partial_sum: Decimal = Decimal(0)
    next_n: int = 0

    def __next__(self) -> Decimal:
        self.partial_sum += (
            ((-1) ** self.next_n) * Decimal(1) / Decimal(2 * self.next_n + 1)
        )
        self.next_n += 1

        return 4 * self.partial_sum


@dataclass
class MonteCarlo(ApproximationSequence):
    """"""

    number_of_samples: int = 0
    samples_inside_of_unit_circle: int = 0

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


@dataclass
class GaussLegendre(ApproximationSequence):
    a: Decimal = Decimal(1)
    _b: InitVar[Decimal | None] = None
    b: Decimal = Decimal("nan")
    t: Decimal = Decimal(1) / Decimal(4)
    p: Decimal = Decimal(1)

    def __next__(self) -> Decimal:
    def __post_init__(self, _b):
        if _b is None:
            self.b = Decimal(1) / Decimal(2).sqrt()
        else:
            self.b = _b

        a = (self.a + self.b) / 2
        self.b = (self.a * self.b).sqrt()
        self.t = self.t - self.p * (self.a - a) ** 2
        self.p = 2 * self.p
        self.a = a
        return ((self.a + self.b) ** 2) / (4 * self.t)


@dataclass
class Chudnovsky(ApproximationSequence):
    partial_sum: Decimal = Decimal(0)
    next_n: int = 0
    _c: InitVar[Decimal | None] = None
    c: Decimal = Decimal("nan")

    def __next__(self) -> Decimal:
    def __post_init__(self, _c):
        if _c is None:
            self.c = Decimal(426880) * Decimal(10005).sqrt()
        else:
            self.c = _c

        self.partial_sum += Decimal(
            factorial(6 * self.next_n) * (13591409 + 545140134 * self.next_n)
        ) / Decimal(
            factorial(3 * self.next_n)
            * factorial(self.next_n) ** 3
            * (-640320) ** (3 * self.next_n)
        )
        self.next_n += 1

        return self.c * (1 / self.partial_sum)


APPROXIMATION_SEQUENCES: dict[str, type] = {
    "Leibniz": Leibniz,
    "MonteCarlo": MonteCarlo,
    "GaussLegendre": GaussLegendre,
    "Chudnovsky": Chudnovsky,
}
