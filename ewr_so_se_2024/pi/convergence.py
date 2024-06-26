import click
from matplotlib import pyplot as plt
from numpy import logspace
from tqdm import tqdm

from ewr_so_se_2024.pi import utils
from ewr_so_se_2024.pi.sequences import APPROXIMATION_SEQUENCES


def calculate_first_mismatches(sequence, sample_points, sequence_name):
    """Calculate the first mismatches for the given sequence and sample points."""
    return [
        utils.find_first_mismatch(sequence.at(k).as_tuple()[1], utils.PI.as_tuple()[1])
        for k in tqdm(
            sample_points,
            desc=f"Calculating convergence of {sequence_name} sequence",
        )
    ]


@click.command("convergence", context_settings={"show_default": True})
@utils.sequence_names
@utils.samples
@utils.export_to
@click.option(
    "--precision",
    type=click.IntRange(min=1),
    default=50,
    help="The precision to use for decimal calculations.",
)
@click.option(
    "--stop",
    type=click.IntRange(min=1, max=12),
    default=4,
    help="The maximum exponent for the logarithmic scale of the sequence positions.",
)
def main(sequence_names, precision, stop, number_of_samples, export_to):
    """
    Perform a convergence analysis of Pi approximation methods.

    This script calculates the number of correctly approximated digits of Pi
    for various sequences and plots the results on a logarithmic scale.
    """
    utils.setup_decimal_context(precision)

    sample_points = logspace(0, stop, num=number_of_samples, dtype=int)

    plt.figure(figsize=(10, 6))

    for sequence_name in tqdm(sequence_names, desc="Processing sequences"):
        sequence = APPROXIMATION_SEQUENCES[sequence_name]()

        first_mismatches = calculate_first_mismatches(
            sequence, sample_points, sequence_name
        )
        plt.loglog(
            sample_points,
            [
                float("+inf") if first_mismatch is None else first_mismatch[0] - 1
                for first_mismatch in first_mismatches
            ],
            label=sequence_name,
            **utils.get_color_and_marker(sequence_name, number_of_samples),
        )

    plt.xlabel("Position within the sequence (log scale)")
    plt.ylabel("Number of correctly approximated digits (log scale)")
    plt.title("Convergence analysis of Pi Approximation Methods")
    plt.legend()
    # Add grid lines
    plt.grid(linestyle="--", linewidth=0.5)

    plt.tight_layout()

    if export_to:
        plt.savefig(export_to)
        return

    plt.show()


if __name__ == "__main__":
    main()
