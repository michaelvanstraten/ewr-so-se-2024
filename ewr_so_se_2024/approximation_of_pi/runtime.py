"""
Runtime Analysis of Pi Approximation Sequences CLI

This module provides a command-line interface (CLI) for performing a runtime 
analysis of various Pi approximation sequences. It measures and plots the total 
computation time and average digit computation time for different sequences 
over a range of digits of precision. The results can be displayed or saved to a file.

Usage: approximation-of-pi runtime [OPTIONS]

  Perform runtime analysis on pi approximation sequences.

Options:
  --samples INTEGER RANGE         The number of samples to take from the
                                  underlying sequence.  [default: 20; x>=1]
  -s, --sequence [Leibniz|MonteCarlo|GaussLegendre|Chudnovsky]
                                  The sequence(s) to use for approximation.
                                  [default: Leibniz, MonteCarlo,
                                  GaussLegendre, Chudnovsky]
  --export-to FILE                Export the generated plot to a specified
                                  file.
  --digits INTEGER RANGE          The maximum number of digits to approximate
                                  pi to.  [default: 5; x>=1]
  --help                          Show this message and exit.

Example:
    approximation-of-pi runtime -s Leibniz -s MonteCarlo --digits 100
"""

from dataclasses import dataclass
import time

from tqdm import tqdm
import click
import matplotlib.pyplot as plt
import numpy as np

from ewr_so_se_2024.approximation_of_pi.sequences import (
    APPROXIMATION_SEQUENCES,
    ApproximationSequence,
)
from ewr_so_se_2024.approximation_of_pi import utils


@dataclass
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
        while (
            self.sequence.current_position <= 0
            or (
                first_mismatch := utils.find_first_mismatch(
                    self.sequence.current_approximation.as_tuple()[1],
                    utils.PI.as_tuple()[1],
                )
            )
            and first_mismatch[0] < n
        ):
            operation_start = time.time_ns()
            next(self.sequence)
            self.total_time += time.time_ns() - operation_start

        return self.total_time


@click.command("runtime", context_settings={"show_default": True})
@utils.samples
@utils.sequence_names
@utils.export_to
@utils.digits
# pylint: disable=too-many-locals
def main(sequence_names, digits, number_of_samples, export_to):
    """Perform runtime analysis on pi approximation sequences."""
    # Set precision for Decimal calculations
    utils.setup_decimal_context(digits + 4)

    # Generate a range of sample points for approximation
    sample_points = np.linspace(1, digits, min(number_of_samples, digits), dtype=int)

    fig, (computation_times_ax, average_position_deltas_ax) = plt.subplots(
        1, 2, figsize=(12, 6)
    )
    fig.suptitle("Runtime and Average Digit Time Analysis")

    for sequence_name in tqdm(sequence_names, desc="Sampling sequences"):
        # Create a runtime analysis instance for each sequence
        sequence = APPROXIMATION_SEQUENCES[sequence_name]()
        runtime_analysis = RuntimeAnalysis(sequence)

        computation_time, average_digit_time = zip(
            *[
                (
                    computation_time := runtime_analysis.approximation_up_to(digits)
                    / 10**6,
                    computation_time / digits,
                )
                for digits in tqdm(
                    sample_points, desc=f"Sampling the {sequence_name} sequence"
                )
            ]
        )

        # Plot runtime analysis for the sequence
        computation_times_ax.plot(
            sample_points,
            computation_time,
            label=sequence_name,
            **utils.get_color_and_marker(sequence_name, number_of_samples),
        )
        average_position_deltas_ax.plot(
            sample_points,
            average_digit_time,
            label=sequence_name,
            **utils.get_color_and_marker(sequence_name, number_of_samples),
        )

    # Set plot scale, labels and legends
    computation_times_ax.set_yscale("log")
    computation_times_ax.set_xlabel("Digits of Precision")
    computation_times_ax.set_ylabel("Computation Time (ms) (log scale)")
    computation_times_ax.legend()
    average_position_deltas_ax.set_yscale("log")
    average_position_deltas_ax.set_xlabel("Digits of Precision")
    average_position_deltas_ax.set_ylabel("Average Time (ms) for One Digit (log scale)")
    average_position_deltas_ax.legend()

    # Display the plot
    plt.tight_layout()

    if export_to:
        plt.savefig(export_to)
        return

    plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
