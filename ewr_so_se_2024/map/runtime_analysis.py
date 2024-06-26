"""This script performs runtime analysis for various pi approximation algorithms.

It uses the following algorithms:
- Leibniz series
- Monte Carlo method
- Gauss-Legendre algorithm
- Chudnovsky algorithm

The script measures the time taken to approximate pi to a specified number of decimal places
and plots the results using matplotlib.

Classes:
    RuntimeAnalysis: Records and calculates the time taken to approximate pi using a given sequence.

Functions:
    main: Command-line interface entry point for the runtime analysis.

Usage:
    Run the script with the desired options to perform and plot runtime analysis.
"""

from dataclasses import dataclass
import time
import decimal
import sys

from tqdm import tqdm
import click
import matplotlib.pyplot as plt
import numpy as np

from ewr_so_se_2024.map.sequences import (
    sequence_names,
    APPROXIMATION_SEQUENCES,
    ApproximationSequence,
)
from ewr_so_se_2024.map.utils import PI, equal_up_to, samples


@dataclass(unsafe_hash=True)
class RuntimeAnalysis:
    """Class to analyze the runtime of a pi approximation sequence."""

    sequence: ApproximationSequence
    total_time: float = 0

    def approximation_up_to(self, n: int) -> float:
        """Approximate pi up to n decimal places and record the time taken.

        Args:
            n (int): The number of decimal places to approximate pi to.

        Returns:
            float: The total time taken to achieve the approximation in nanoseconds.
        """
        while not equal_up_to(n, self.sequence.current_approximation, PI):
            operation_start = time.time_ns()
            next(self.sequence)
            self.total_time += time.time_ns() - operation_start

        return self.total_time


@click.command("runtime-analysis")
@sequence_names
@click.option(
    "--digits",
    type=click.IntRange(min=1),
    default=5,
    show_default=True,
    help="The maximum number of digits to approximate pi to.",
)
@samples
# pylint: disable=too-many-locals
def main(sequence_names, digits, number_of_samples):
    """Main function to perform runtime analysis on pi approximation sequences.

    Args:
        sequence_names (list[str]): Names of the sequences to analyze.
        digits (int): Number of digits of precision for pi approximation.
        number_of_samples (int): Number of sample points for the analysis.
    """
    # Set precision for Decimal calculations
    decimal.getcontext().prec = digits + 4
    old_max_str_digits = sys.get_int_max_str_digits()
    # Disable limit on string conversion for integers
    sys.set_int_max_str_digits(0)

    possible_markers = list(".,ov^<>1248spP*hH+xX")
    possible_colors = list("bgrcmykw")

    # Generate a range of sample points for approximation
    sample_points = np.linspace(1, digits, min(number_of_samples, digits), dtype=int)

    fig, (computation_times_ax, average_position_deltas_ax) = plt.subplots(
        2, figsize=(10, 8)
    )
    fig.suptitle("Runtime and Average Digit Time Analysis")

    for sequence_name in tqdm(sequence_names, desc="Sequences Progress"):
        # Create a RuntimeAnalysis instance for each sequence
        sequence = APPROXIMATION_SEQUENCES[sequence_name]()
        runtime_analysis = RuntimeAnalysis(sequence)

        # Determine marker and color for the sequence
        hash_value = hash(sequence_name)
        marker = (
            possible_markers[hash_value % len(possible_markers)]
            if number_of_samples < 100
            else ""
        )
        color = possible_colors[hash_value % len(possible_colors)]

        computation_time, average_digit_time = zip(
            *[
                (
                    computation_time := runtime_analysis.approximation_up_to(digits)
                    / 1000,
                    computation_time / digits,
                )
                for digits in tqdm(sample_points, desc=f"Processing {sequence_name}")
            ]
        )

        # Plot runtime analysis for the sequence
        computation_times_ax.plot(
            sample_points,
            computation_time,
            label=sequence_name,
            marker=marker,
            color=color,
        )
        average_position_deltas_ax.plot(
            sample_points,
            average_digit_time,
            label=sequence_name,
            marker=marker,
            color=color,
        )

    # Restore original max string digits setting
    sys.set_int_max_str_digits(old_max_str_digits)

    # Set plot scale, labels and legends
    computation_times_ax.set_yscale("log")
    computation_times_ax.set_xlabel("Digits of Precision")
    computation_times_ax.set_ylabel("Computation Time (ms)")
    computation_times_ax.legend()
    average_position_deltas_ax.set_yscale("log")
    average_position_deltas_ax.set_xlabel("Digits of Precision")
    average_position_deltas_ax.set_ylabel("Average Time (ms) for One Digit")
    average_position_deltas_ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
