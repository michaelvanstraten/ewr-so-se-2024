""""""

from abc import abstractmethod
from collections import abc
from dataclasses import InitVar, dataclass
from decimal import Decimal
from math import factorial, sqrt


import random

RealValuedSequence = abc.Iterator[Decimal]


@dataclass
class ApproximationSequence(RealValuedSequence):
    _current_position: int = -1
    _current_approximation: Decimal = Decimal("nan")

    @property
    def current_position(self) -> int:
        return self._current_position

    @property
    def current_approximation(self) -> Decimal:
        return self._current_approximation

    def __iter__(self) -> Iterator[Decimal]:
        return self

    def __next__(self) -> Decimal:
        self._current_position += 1
        self._current_approximation = self.next_element()
        return self._current_approximation

    @abstractmethod
    def next_element(self) -> Decimal:
        pass

@dataclass
    def at(self, position: int) -> Union[Decimal, None]:
        if self.current_position > position:
            return None

        while self.current_position < position:
            next(self)

        return self.current_approximation


class Leibniz(ApproximationSequence):
    partial_sum: Decimal = Decimal(0)

    def next_element(self) -> Decimal:
        self.partial_sum += (
            ((-1) ** self.current_position)
            * Decimal(1)
            / Decimal(2 * self.current_position + 1)
        )

        return 4 * self.partial_sum


@dataclass
class MonteCarlo(ApproximationSequence):
    """"""

    samples_inside_of_unit_circle: int = 0

    def next_element(self) -> Decimal:
        random_x, random_y = random.random(), random.random()
        if sqrt(random_x**2 + random_y**2) <= 1:
            self.samples_inside_of_unit_circle += 1
        return (
            4
            * Decimal(self.samples_inside_of_unit_circle)
            / Decimal(self.current_position + 1)
        )


@dataclass
class GaussLegendre(ApproximationSequence):
    a: Decimal = Decimal(1)
    _b: InitVar[Decimal | None] = None
    b: Decimal = Decimal("nan")
    t: Decimal = Decimal(1) / Decimal(4)
    p: Decimal = Decimal(1)

    def __post_init__(self, _b):
        if _b is None:
            self.b = Decimal(1) / Decimal(2).sqrt()
        else:
            self.b = _b

    def next_element(self) -> Decimal:
        a = (self.a + self.b) / 2
        self.b = (self.a * self.b).sqrt()
        self.t = self.t - self.p * (self.a - a) ** 2
        self.p = 2 * self.p
        self.a = a
        return ((self.a + self.b) ** 2) / (4 * self.t)


@dataclass
class Chudnovsky(ApproximationSequence):
    partial_sum: Decimal = Decimal(0)
    _c: InitVar[Decimal | None] = None
    c: Decimal = Decimal("nan")

    def __post_init__(self, _c):
        if _c is None:
            self.c = Decimal(426880) * Decimal(10005).sqrt()
        else:
            self.c = _c

    def next_element(self) -> Decimal:
        self.partial_sum += Decimal(
            factorial(6 * self.current_position)
            * (13591409 + 545140134 * self.current_position)
        ) / Decimal(
            factorial(3 * self.current_position)
            * factorial(self.current_position) ** 3
            * (-640320) ** (3 * self.current_position)
        )

        return self.c * (1 / self.partial_sum)


APPROXIMATION_SEQUENCES: dict[str, type] = {
    "Leibniz": Leibniz,
    "MonteCarlo": MonteCarlo,
    "GaussLegendre": GaussLegendre,
    "Chudnovsky": Chudnovsky,
}

if __name__ == "__main__":
    print(
        f"It follows a calculation of the 20th partial sum of the {', '.join(APPROXIMATION_SEQUENCES.keys())} pi approximation sequence:"
    )

    sequences = [sequence() for sequence in APPROXIMATION_SEQUENCES.values()]

    for _ in range(20):
        for sequence in sequences:
            next(sequence)

    print(*sequences, sep="\n")
