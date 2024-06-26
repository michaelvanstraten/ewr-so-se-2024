"""This module provides utility functions and options for pi approximation analysis.

Functions:
    equal_up_to: Check if two Decimal numbers are equal up to a specified number of digits.

Variables:
    PI: The value of pi read from a file and stored as a Decimal.
    number_of_samples: Click option for specifying the number of samples to take from the sequence.
"""

import sys
from decimal import Decimal
from os import path
import click

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


# Click option for specifying the number of samples to take from the sequence
samples = click.option(
    "--samples",
    "number_of_samples",
    type=click.IntRange(min=1),
    default=20,
    show_default=True,
    help="The number of samples to take from the underlying sequence.",
)
