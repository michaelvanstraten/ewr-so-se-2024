"""
This module provides a command-line interface (CLI) for generating or loading a harmonic sequence
and performing summation using different algorithms and data types. 
The results can be optionally displayed and saved to a file.
"""

import numpy as np
import matplotlib.pyplot as plt
import click
import tikzplotlib
from yaspin import yaspin

from ewr_so_se_2024.utils import NotRequiredIf, tikzplotlib_fix_ncols
from ewr_so_se_2024.harmonic_convergence import (
    harmonic_sum,
    forward_sum,
    kahan_sum,
    vectorized_sum,
)
from ewr_so_se_2024.tools_read_save import load_data, save_data
from ewr_so_se_2024.py_logspace import py_logspace


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
    help="The starting point from which to calculate the logspace.",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the starting point of the logspace:",
)
@click.option(
    "--stop",
    type=click.IntRange(min=1, max=12),
    default=5,
    help="The end point from which to calculate the logspace.",
    cls=NotRequiredIf,
    not_required_if="load",
    prompt="Enter the end point of the logspace:",
)
@click.option(
    "-n",
    "--number-of-terms",
    type=click.IntRange(min=2),
    default=20,
    help="Number of terms to generate or load.",
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
    help="The data type to use for summing.",
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
    help="The algorithm to use for summation.",
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
    help="Load data from a specified file.",
)
@click.option(
    "-s",
    "--save",
    type=click.Path(dir_okay=False, writable=True),
    help="Save the generated data to a specified file.",
)
@click.option(
    "--export-as-tex",
    type=click.Path(dir_okay=False, writable=True),
    help="Export the generated data to a specified file using `tikzplotlib`.",
)
# pylint: disable=too-many-arguments
def main(
    start,
    stop,
    number_of_terms,
    data_type,
    summation_algorithm,
    display,
    load,
    save,
    export_as_tex,
):
    """
    Generate or load harmonic sequence and perform summation.
    """
    if load is not None:
        # Load data if specified
        sequence_elements, (
            start,
            stop,
            number_of_terms,
            data_type,
            summation_algorithm,
        ) = load_data(load)
    else:
        # Generate harmonic sequence
        with yaspin(text="Calculating harmonic sums...", color="yellow") as spinner:
            # Ignore overflow errors when operation on numpy data
            np.seterr(over="ignore")
            sequence_elements = harmonic_sum(
                start,
                stop,
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

    if display or export_as_tex is not None:
        plt.subplots_adjust(left=0.2, right=0.5)
        fig = plt.figure("Harmonic Sum Convergence", figsize=(10, 6))

        # Plot the generated data
        plt.loglog(
            py_logspace(start, stop, number_of_terms),
            sequence_elements,
            label=f"{summation_algorithm} summation using {data_type}",
            marker="o",
        )

        # Add labels and legend
        plt.xlabel("Number of Terms (log scale)")
        plt.ylabel("Harmonic Sum (log scale)")

        plt.legend()

        # Issue with tikzplotlib https://stackoverflow.com/a/75903189
        tikzplotlib_fix_ncols(fig)

        if display:
            # Show plot
            plt.show()
        if export_as_tex:
            tikzplotlib.save(export_as_tex)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
