"""This module provides utility functions and options for pi approximation analysis.

Functions:
    find_first_mismatch: Find the first mismatch between two iterables.

Variables:
    PI: The value of pi read from a file and stored as a Decimal.
    number_of_samples: Click option for specifying the number of samples to take from the sequence.
"""

from collections.abc import Iterable
from itertools import zip_longest
import sys
from decimal import Decimal
from os import path
from typing import Optional, TypeVar
import decimal

import click

from ewr_so_se_2024.pi.sequences import APPROXIMATION_SEQUENCES

# Click option for specifying the number of samples to take from the sequence
samples = click.option(
    "--samples",
    "number_of_samples",
    type=click.IntRange(min=1),
    default=20,
    help="The number of samples to take from the underlying sequence.",
)

# Click option for specifying the sequence names to analyse
sequence_names = click.option(
    "-s",
    "--sequence",
    "sequence_names",
    type=click.Choice(list(APPROXIMATION_SEQUENCES.keys()), case_sensitive=False),
    default=list(APPROXIMATION_SEQUENCES.keys()),
    multiple=True,
    help="The sequence(s) to use for approximation.",
)

# Load the value of PI from a file and store it as a Decimal
with open(path.join(path.dirname(__file__), "PI"), encoding="utf-8") as PI_file:
    old_max_str_digits = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    PI = Decimal(PI_file.read().translate(str.maketrans("", "", "\n\r\t ")))
    sys.set_int_max_str_digits(old_max_str_digits)


AItem = TypeVar("AItem")
BItem = TypeVar("BItem")


def find_first_mismatch(
    xs: Iterable[AItem], ys: Iterable[BItem]
) -> Optional[tuple[int, AItem, BItem]]:
    """Find the first mismatch between two iterables.

    Args:
        xs: The first iterable.
        ys: The second iterable.

    Returns:
        A tuple containing the index of the first mismatch and the mismatched items, \
        or None if no mismatch is found.
    """
    for idx, (x, y) in enumerate(zip_longest(xs, ys)):
        if x != y:
            return idx, x, y
    return None


def get_color_and_marker(sequence_name: str, number_of_samples: int) -> dict:
    """Utility function to get color and marker based on sequence name.

    Args:
        sequence_name (str): The name of the sequence.
        number_of_samples (int): The number of samples.

    Returns:
        Tuple[str, str]: A tuple containing the color and marker.
    """
    possible_markers = list(".,ov^<>1248spP*hH+xX")
    possible_colors = list("bgrcmykw")

    hash_value = hash(sequence_name)
    marker = (
        possible_markers[hash_value % len(possible_markers)]
        if number_of_samples < 100
        else ""
    )
    color = possible_colors[hash_value % len(possible_colors)]

    return {"color": color, "marker": marker}


def setup_decimal_context(precision: int):
    """Set up the decimal context with the given precision.

    Args:
        precision (int): The precision to set for the decimal context.
    """
    sys.set_int_max_str_digits(0)
    decimal.getcontext().prec = precision
