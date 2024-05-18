import numpy as np
from harmonic_convergence import harmonic_sum
import tools_read_save as trs
import matplotlib as plt


def main():
    """
    docstring
    """
    wahl = input("Wollen sie eigene Parameter eingeben (1), Standardparameter verwenden (2), oder Parameter aus einer Datei laden (3) ")
    if wahl == "1":
        n = int(input("Geben sie die Zahl ein bis zu der aufsummiert werden soll: "))
        method = input("Wählen sie ihre Summationsmethode: Forward/Kahan: ")
        dtype = input("Geben sie den Datentyp der Zahlen ein: ")
        summe = harmonic_sum(n, method, eval(dtype))
        print(summe)
    elif wahl == "2":
                n = 10
                method = "Forward"
                summe = harmonic_sum(n, method)
                print(summe)
    elif wahl == "3":
                name = input("Geben sie den Namen der Datei, die geladen werden soll, ein: ")


if __name__ == "__main__":
       main()

