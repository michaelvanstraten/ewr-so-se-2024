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
    list = py_logspace(1, n, n)
    sum = dtype(0)
    for i in range(0, n-1):
        tmp = np.log10(list[i])
        sum += (dtype(1)/dtype(tmp))
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
    c = dtype(0)  # Korrekturterm
    for k in range(1, n + 1):
        y = dtype(1) / dtype(k) - c
        t = sum + y
        c = (t - sum) - y
        sum = t
    return sum

def harmonic_sum(n:int, method, dtype=np.float32):
    """
    Bestimmung der Summationsmethode zur Berechnung der n-ten Harmonischen Summe
    von M. van Straten und P. Merz
    params: n - Bestimmung der n-ten Harmonischen Summe
            dtype - Datentyp der Summanden. Standardmäßig np.float32
    returns: n-te Harmonische Summe
    """
    if method == "Kahan":
        return kahan_sum(n, dtype)
    elif method =="Forward":
        return forward_sum(n, dtype)
    else:
        raise NameError("Invalide Methode")

# Beispiele
#print(forward_sum(10))
#print(kahan_sum(10))
#print(harmonic_sum(10, "Forward", np.float64))
#print(harmonic_sum(10, "Kahan", np.float16))
#