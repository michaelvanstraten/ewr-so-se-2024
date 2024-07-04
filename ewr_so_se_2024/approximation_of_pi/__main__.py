import click

from ewr_so_se_2024.approximation_of_pi import (
    memory,
    runtime,
    convergence,
)


@click.group()
def cli():
    pass


cli.add_command(runtime.main)
cli.add_command(convergence.main)
cli.add_command(memory.plot_memory_usage)

if __name__ == "__main__":
    cli()
