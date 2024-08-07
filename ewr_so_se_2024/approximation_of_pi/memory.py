"""
Memory Usage Analysis of Pi Approximation Sequences CLI

This module provides a command-line interface (CLI) for analyzing the memory usage 
of various Pi approximation sequences over a range of digits of precision. It plots 
the memory size of different sequences and can display the plot or save it to a file.

Usage: approximation-of-pi plot-memory-usage [OPTIONS]

  Plot the memory usage of different Pi approximation sequences over a range
  of digits of precision.

Options:
  -s, --sequence [Leibniz|MonteCarlo|GaussLegendre|Chudnovsky]
                                  The sequence(s) to use for approximation.
  --digits INTEGER RANGE          The maximum number of digits to approximate
                                  pi to.  [x>=1]
  --samples INTEGER RANGE         The number of samples to take from the
                                  underlying sequence.  [x>=1]
  --export-to FILE                Export the generated plot to a specified
                                  file.
  --help                          Show this message and exit.

Example:
    approximation-of-pi plot-memory-usage -s Leibniz -s MonteCarlo --digits 100

"""

import decimal
import pickle

import numpy as np
import click
from matplotlib import pyplot as plt

from ewr_so_se_2024.approximation_of_pi import utils
from ewr_so_se_2024.approximation_of_pi.sequences import (
    APPROXIMATION_SEQUENCES,
    ApproximationSequence,
)

# Mapping of sequences to their appropriate starting positions
SEQUENCE_POSITIONS = {
    "Leibniz": 128,
    "GaussLegendre": 0,
    "Chudnovsky": 0,
    "MonteCarlo": 1024,
}


def calculate_sequence_memory_size(
    sequence_class: type[ApproximationSequence], precision: int, position: int
) -> int:
    """
    Calculate the memory size of a given sequence at a specified position and precision.

    Args:
        sequence_class: The approximation sequence class.
        precision: The precision (number of digits) for the decimal context.
        position: The position in the sequence to evaluate.

    Returns:
        The memory size of the sequence instance in bytes.
    """
    with decimal.localcontext(prec=precision):
        sequence_instance = sequence_class()
        sequence_instance.at(position)
        # The pickled version of the object roughly has the same memory
        # footprint of the underlying type
        return len(pickle.dumps(sequence_instance))


@click.command("memory-usage")
@utils.sequence_names
@utils.digits
@utils.samples
@utils.export_to
def plot_memory_usage(sequence_names, digits, number_of_samples, export_to):
    """
    Plot the memory usage of different Pi approximation sequences
    over a range of digits of precision.
    """
    # Generate a range of sample points for approximation
    precision_range = np.linspace(1, digits, min(number_of_samples, digits))

    for sequence_name in sequence_names:
        memory_sizes = [
            calculate_sequence_memory_size(
                APPROXIMATION_SEQUENCES[sequence_name],
                int(precision),
                SEQUENCE_POSITIONS[sequence_name],
            )
            for precision in precision_range
        ]
        plt.plot(
            precision_range,
            memory_sizes,
            label=sequence_name,
            **utils.get_color_and_marker(sequence_name, number_of_samples)
        )

    plt.legend()
    plt.xlabel("Digits of Precision")
    plt.ylabel("Memory Size (bytes)")
    plt.title("Memory Usage of Pi Approximation Sequences")
    plt.grid(True)

    if export_to:
        plt.savefig(export_to)
        return

    plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    plot_memory_usage()
