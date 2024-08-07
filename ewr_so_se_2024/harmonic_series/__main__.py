"""
This module provides a command-line interface (CLI) for generating or loading a harmonic sequence
and performing summation using different algorithms and data types. 
The results can be optionally displayed and saved to a file.
"""

import numpy as np
import matplotlib.pyplot as plt
import click
from yaspin import yaspin

from ewr_so_se_2024.harmonic_series.utils import NotRequiredIf
from ewr_so_se_2024.harmonic_series.harmonic_convergence import (
    harmonic_sum,
    forward_sum,
    kahan_sum,
    vectorized_sum,
)
from ewr_so_se_2024.harmonic_series.tools_read_save import load_data, save_data
from ewr_so_se_2024.harmonic_series.py_logspace import py_logspace


# Define available summation algorithms and data types
SUMMATION_ALGORITHMS = {
    "Forward": forward_sum,
    "Kahan": kahan_sum,
    "Vectorized": vectorized_sum,
}
DATA_TYPES = {"float16": np.float16, "float32": np.float32, "float64": np.float64}


@click.command()
@click.option(
    "--start",
    type=click.IntRange(min=0, max=12),
    default=0,
    show_default=True,
    help="The starting exponent for calculating the logspace (base ^ start).",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the starting exponent of the logspace:",
)
@click.option(
    "--stop",
    type=click.IntRange(min=1, max=12),
    default=5,
    show_default=True,
    help="The ending exponent for calculating the logspace (base ^ stop).",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the ending exponent of the logspace:",
)
@click.option(
    "--basis",
    type=click.IntRange(min=2),
    default=10,
    show_default=True,
    help="The base for the logspace calculation.",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the base for the logspace:",
)
@click.option(
    "-n",
    "--number-of-terms",
    type=click.IntRange(min=2),
    default=20,
    help="Number of terms to generate or load.",
    show_default=True,
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the number of terms:",
)
@click.option(
    "-t",
    "--data-type",
    type=click.Choice(list(DATA_TYPES.keys())),
    default="float64",
    show_default=True,
    help="The data type to use for summing (float16, float32, float64).",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Choose the data type for summing:",
)
@click.option(
    "-a",
    "--summation-algorithm",
    type=click.Choice(list(SUMMATION_ALGORITHMS.keys()), case_sensitive=False),
    default="Forward",
    show_default=True,
    help="The algorithm to use for summation (Forward, Kahan, Vectorized).",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Choose the summation algorithm:",
)
@click.option(
    "--display/--no-display",
    is_flag=True,
    default=True,
    show_default=True,
    help="Display the generated or loaded data.",
)
@click.option(
    "-l",
    "--load",
    type=click.Path(exists=True, dir_okay=False),
    help="Load data from a specified JSON file.",
)
@click.option(
    "-s",
    "--save",
    type=click.Path(dir_okay=False, writable=True),
    help="Save the generated data to a specified JSON file. Note: Provide the .json extension.",
)
@click.option(
    "--export-to",
    type=click.Path(dir_okay=False, writable=True),
    help="Export the generated plot to a specified file.",
)
# pylint: disable=too-many-arguments
def main(
    start,
    stop,
    basis,
    number_of_terms,
    data_type,
    summation_algorithm,
    display,
    load,
    save,
    export_to,
):
    """
    Generate or load a harmonic sequence and perform summation.
    """
    if load is not None:
        # Load data if specified
        sequence_elements, (
            start,
            stop,
            basis,
            number_of_terms,
            data_type,
            summation_algorithm,
        ) = load_data(load)
    else:
        # Generate harmonic sequence
        with yaspin(text="Calculating harmonic sums...", color="yellow") as spinner:
            # Ignore overflow errors when operating on NumPy data
            np.seterr(over="ignore")
            sequence_elements = harmonic_sum(
                start,
                stop,
                basis,
                number_of_terms,
                SUMMATION_ALGORITHMS[summation_algorithm],
                DATA_TYPES[data_type],
            )
            spinner.ok("✅")

    if save is not None:
        # Save the generated sequence
        save_data(
            save,
            list(map(float, sequence_elements)),
            start,
            stop,
            number_of_terms,
            data_type,
            summation_algorithm,
        )

    if display or export_to is not None:
        plt.figure("Harmonic Sum Convergence", figsize=(10, 6))

        # Plot the generated data
        plt.loglog(
            py_logspace(start, stop, number_of_terms),
            sequence_elements,
            label=f"{summation_algorithm} summation using {data_type}",
            marker="o" if number_of_terms <= 100 else "",
        )

        # Add labels and legend
        plt.xlabel("Number of Terms (log scale)")
        plt.ylabel("Harmonic Sum (log scale)")
        plt.title("Harmonic Series Summation Convergence")
        plt.legend()

        if export_to:
            plt.savefig(export_to)
        if display:
            # Show plot
            plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
