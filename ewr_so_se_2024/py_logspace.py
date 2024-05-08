"""
Aufgabe 2.1: Logspace mit ganzen Zahlen in Python berechnen
"""

from typing import Any, cast

import click
from numpy import ndarray
import matplotlib.pyplot as plt


def py_logspace(
    start: int, stop: int, num: int = 5, basis: int = 10, dtype: Any = int
) -> list[int]:
    """
    Erstellung von Liste ganzer Zahlen mit logarithmisch konstantem Abstand
    von M. van Straten und P. Merz
    params: start - Legt kleinstes Element der auszugebenden Liste mit basis^start fest
            stop  - Legt größtes Element der auszugebenden Liste mit basis^stop fest
            num   - Anzahl der Elemente in der auszugebenden Liste
            basis - Legt mit start und stop erstes und letztes Element fest, standardmäßig = 10
    returns: Liste mit num Anzahl an Elementen zwischen basis^start und basis^stop
    """
    if num < 2:
        raise ValueError
    exp_liste = (
        []
    )  # Leere Liste wird erstellt, die später mit den gesuchten Elementen gefüllt wird
    for i in range(0, num):  # Iteratives Erstellen neuer ELemente
        step = (stop - start) / (
            num - 1
        )  # step ist der logarithmisch gesehene konstante Abstand
        log_add = start + i * step  # logarithmischer konstanter Abstand wird addiert
        exp_add = dtype(basis**log_add)  # Neues Element für die Liste wird erstellt
        exp_liste.append(exp_add)  # Das neue Element wird zur Liste hinzugefügt
    return exp_liste


@click.command()
@click.argument("start", type=int)
@click.argument("stop", type=int)
@click.option("-s", "--number-of-samples", default=5, type=int)
@click.option("--basis", default=10, type=float)
def main(start, stop, number_of_samples, basis):
    """
    Samples `py_logspace` with the given input and then plots the result using matplotlib.
    """
    samples = py_logspace(start, stop, num=number_of_samples, basis=basis)

    fig = plt.figure(
        f"py_logspace({start}, {stop}, num={number_of_samples}, basis={basis})"
    )
    axis_one, axis_two = cast(ndarray, fig.subplots(nrows=1, ncols=2))
    axis_one.plot(samples)
    axis_two.plot(samples)
    axis_two.set_yscale("log")

    plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
