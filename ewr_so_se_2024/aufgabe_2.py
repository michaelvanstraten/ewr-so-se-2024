from functools import partial
from itertools import accumulate, repeat

from typing import Any

import click


def py_logspace(
    start: int, stop: int, num: int = 5, basis: int = 10, dtype: Any = int
) -> list:
    if num < 3:
        raise ValueError
    offset = repeat((stop - start) / (num - 1), num - 1)
    # Would be cleaner with https://github.com/EntilZha/PyFunctional
    items = map(dtype, map(partial(pow, basis), accumulate(offset, initial=start)))
    # Would be more efficiant if they let us return an iterator instead of a list
    return list(items)


@click.command()
@click.argument("start", type=int)
@click.argument("stop", type=int)
@click.option("-s", "--number-of-samples", default=5, type=int)
@click.option("--basis", default=10, type=float)
def main(start, stop, number_of_samples, basis):
    import matplotlib.pyplot as plt

    sample = py_logspace(start, stop, num=number_of_samples, basis=basis)

    fig = plt.figure(
        f"py_logspace({start}, {stop}, num={number_of_samples}, basis={basis})"
    )
    axes = fig.subplots(nrows=1, ncols=2)
    axes[0].plot(sample)
    axes[1].plot(sample)
    axes[1].set_yscale("log")

    plt.show()


if __name__ == "__main__":
    main()
