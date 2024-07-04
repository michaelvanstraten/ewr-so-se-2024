# pylint: disable=missing-module-docstring; (since this is the `__main__` module)

import click

from ewr_so_se_2024.approximation_of_pi import (
    memory,
    runtime,
    convergence,
)


@click.group()
def cli():
    """
    Command-line interface for the approximation of Pi report for the EWR (SoSe2024) course.

    This CLI provides commands to run various modules related to the approximation of Pi,
    including runtime analysis, convergence analysis, and memory usage plotting.
    """


cli.add_command(runtime.main, name="runtime")
cli.add_command(convergence.main, name="convergence")
cli.add_command(memory.plot_memory_usage, name="plot-memory-usage")

# Note that the `__name__ == "__main__"` expression is not required here since
# this module is only loaded if somebody loads it as the top level module.
cli()
