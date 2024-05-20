import numpy as np
from py_logspace import py_logspace


def forward_sum(n: int, dtype=np.float32):
    """
    Berechnung n-ter Harmonischer Summe mittels Vorwärtssummation
    von M. van Straten und P. Merz
    params: n - Bestimmung der n-ten Harmonischen Summe
            dtype - Datentyp der Summanden. Standardmäßig np.float32
    returns: n-te Harmonische Summe
    """
    sum = dtype(0)
    for i in range(1, n + 1):
        sum += dtype(1) / dtype(i)
    return sum


def kahan_sum(n: int, dtype=np.float32):
    """
    Berechnung n-ter Harmonischer Summe mittels Kahan-Summation
    von M. van Straten und P. Merz
    params: n - Bestimmung der n-ten Harmonischen Summe
            dtype - Datentyp der Summanden. Standardmäßig np.float32
    returns: n-te Harmonische Summe
    """
    sum = dtype(0)
    # Korrekturterm
    c = dtype(0)
    for k in range(1, n + 1):
        y = dtype(1) / dtype(k) - c
        t = sum + y
        c = (t - sum) - y
        sum = t
    return sum


def harmonic_sum(n: int, method, dtype=np.float32):
    """
    Bestimmung der Summationsmethode zur Berechnung der n-ten Harmonischen Summe
    von M. van Straten und P. Merz
    params: n - Anzahl der Folgegliedern der Harmonischen Reihe, im logarithmischen Abstand
            dtype - Datentyp der Summanden. Standardmäßig np.float32
    returns:
    """
    A = py_logspace(1, 5, n)
    B = []
    for i in range(0, n):
        tmp = A[i]
        B.append(method(tmp, dtype))
    return B


def main():
    print(harmonic_sum(10, kahan_sum, np.float32))
    print(harmonic_sum(5, forward_sum, np.float32))


if __name__ == "__main__":
    main()
