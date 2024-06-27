import click

from ewr_so_se_2024.pi import (
    runtime,
    convergence,
)


@click.group()
def cli():
    pass


cli.add_command(runtime.main)
cli.add_command(convergence.main)

if __name__ == "__main__":
    cli()
