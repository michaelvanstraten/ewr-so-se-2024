"""
Pi Approximation Sequences

This module provides various classes for approximating the value of Pi using different
sequences and algorithms. It also includes an example command-line interface (CLI) 
to run the approximations and display the results.

Classes:
    ApproximationSequence: Abstract base class for Pi approximation sequences.
    Leibniz: Implements the Leibniz series for Pi approximation.
    MonteCarlo: Implements the Monte Carlo method for Pi approximation.
    GaussLegendre: Implements the Gauss-Legendre algorithm for Pi approximation.
    Chudnovsky: Implements the Chudnovsky algorithm for Pi approximation.

Attributes:
    APPROXIMATION_SEQUENCES (dict): A dictionary mapping sequence names to their classes.
"""

import decimal
import random
from abc import ABC, abstractmethod
from collections import abc
from dataclasses import InitVar, dataclass
from decimal import Decimal
from math import factorial, sqrt
from typing import Iterator, Union

import click

RealValuedSequence = abc.Iterator[Decimal]


@dataclass
class ApproximationSequence(ABC, RealValuedSequence):
    """Abstract base class for a sequence that approximates the value of pi."""

    _current_position: int = -1
    _current_approximation: Decimal = Decimal("nan")

    @property
    def current_position(self) -> int:
        """Returns the current position in the sequence."""
        return self._current_position

    @property
    def current_approximation(self) -> Decimal:
        """Returns the current approximation of pi."""
        return self._current_approximation

    def __iter__(self) -> Iterator[Decimal]:
        """Returns an iterator for the sequence."""
        return self

    def __next__(self) -> Decimal:
        """Advances to the next element in the sequence and returns it."""
        self._current_position += 1
        self._current_approximation = self.next_element()
        return self._current_approximation

    @abstractmethod
    def next_element(self) -> Decimal:
        """Calculates the next element in the sequence. Must be implemented by subclasses."""

    def at(self, position: int) -> Union[Decimal, None]:
        """Returns the approximation at a specific position in the sequence.

        Args:
            position (int): The position in the sequence.

        Returns:
            Decimal: The approximation at the specified position, or None if
                     the position has already been passed.
        """
        if self.current_position > position:
            return None

        while self.current_position < position:
            next(self)

        return self.current_approximation


@dataclass
class Leibniz(ApproximationSequence):
    """Leibniz series for pi approximation."""

    partial_sum: Decimal = Decimal(0)

    def next_element(self) -> Decimal:
        """Calculates the next element in the Leibniz series."""
        self.partial_sum += (
            (-1 if self.current_position % 2 == 1 else 1)
            * Decimal(1)
            / Decimal(2 * self.current_position + 1)
        )
        return 4 * self.partial_sum


@dataclass
class MonteCarlo(ApproximationSequence):
    """Monte Carlo method for pi approximation."""

    samples_inside_of_unit_circle: int = 0
    generator = random.Random(420)

    def next_element(self) -> Decimal:
        """Generates a random sample and updates the pi approximation."""
        random_x, random_y = self.generator.random(), self.generator.random()
        if sqrt(random_x**2 + random_y**2) <= 1:
            self.samples_inside_of_unit_circle += 1
        return (
            4
            * Decimal(self.samples_inside_of_unit_circle)
            / Decimal(self.current_position + 1)
        )


@dataclass
class GaussLegendre(ApproximationSequence):
    """Gauss-Legendre algorithm for pi approximation."""

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
        """Calculates the next element in the Gauss-Legendre algorithm."""
        precision = decimal.getcontext().prec
        if precision < self.current_position or precision < 2**self.current_position:
            return self.current_approximation

        a = (self.a + self.b) / 2
        self.b = (self.a * self.b).sqrt()
        self.t = self.t - self.p * (self.a - a) ** 2
        self.p = 2 * self.p
        self.a = a
        return ((self.a + self.b) ** 2) / (4 * self.t)


@dataclass
class Chudnovsky(ApproximationSequence):
    """Chudnovsky algorithm for pi approximation."""

    partial_sum: Decimal = Decimal(0)
    _c: InitVar[Decimal | None] = None
    c: Decimal = Decimal("nan")

    def __post_init__(self, _c):
        if _c is None:
            self.c = Decimal(426880) * Decimal(10005).sqrt()
        else:
            self.c = _c

    def next_element(self) -> Decimal:
        """Calculates the next element in the Chudnovsky algorithm."""
        if decimal.getcontext().prec < 14 * self.current_position:
            return self.current_approximation

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


@click.command()
def main():
    """Run the approximations and display the results."""
    for sequence_name, sequence_class in APPROXIMATION_SEQUENCES.items():
        sequence = sequence_class()
        print(
            f"The 20th approximation of the {sequence_name} sequence is: {sequence.at(20)}."
        )


if __name__ == "__main__":
    main()
