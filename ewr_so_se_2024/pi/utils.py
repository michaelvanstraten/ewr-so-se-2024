"""This module provides utility functions and options for pi approximation analysis.

Functions:
    find_first_mismatch: Find the first mismatch between two iterables.
    setup_decimal_context: Set up the decimal context with the given precision.

Variables:
    PI: The value of pi read from a file and stored as a Decimal.
    number_of_samples: Click option for specifying the number of samples to take from the sequence.
"""

import sys
from decimal import Decimal
from os import path
from typing import Optional, TypeVar
import decimal

import click

# Click option for specifying the number of samples to take from the sequence
samples = click.option(
    "--samples",
    "number_of_samples",
    type=click.IntRange(min=1),
    default=20,
    help="The number of samples to take from the underlying sequence.",
)

# Load the value of PI from a file and store it as a Decimal
with open(path.join(path.dirname(__file__), "PI"), encoding="utf-8") as PI_file:
    old_max_str_digits = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    PI = Decimal(PI_file.read().translate(str.maketrans("", "", "\n\r\t ")))
    sys.set_int_max_str_digits(old_max_str_digits)


def equal_up_to(n: int, a: Decimal, b: Decimal) -> bool:
    """Check if two Decimal numbers are equal up to n decimal places.

    Args:
        n (int): The number of decimal places to check.
        a (Decimal): The first Decimal number.
        b (Decimal): The second Decimal number.

    Returns:
        bool: True if the numbers are equal up to n decimal places, False otherwise.
    """
    digits_a = a.as_tuple()[1]
    digits_b = b.as_tuple()[1]
    point_to_check = min(len(digits_a), n)

    # Check if the length of digits up to the point_to_check is the same for both numbers
    if point_to_check != min(len(digits_b), n):
        return False

    return digits_a[:point_to_check] == digits_b[:point_to_check]
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
