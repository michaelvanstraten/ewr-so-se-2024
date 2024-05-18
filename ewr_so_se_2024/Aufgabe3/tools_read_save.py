import json
from os import PathLike

def read_number(question: str, data_type: type, lower_limit: float = float("-Inf"), upper_limit: float = float("Inf")) -> "data_type":
    """
    Einlesen von Zahlen
    von M. van Straten und P. Merz
    params: question - Aufforderung an den Nutzer
            data_type - Datentyp, die vom Nutzer erwartet wird
            lower_limit - Untere valide Grenze der Eingabe
            upper_limit - Obere valide Grenze der Eingabe
    returns: Eingabe im Typ data_type
    """
    while True:
        answer = input(question)
        try:
            # Überprüfung ob Eingabe des Nutzers dem gewünschten Datentyp entspricht
            input_value = data_type(answer)
            # Überprüfung ob Eingabe des Nutzers innerhalb der Grenzen liegt
            if lower_limit <= input_value <= upper_limit:
                return input_value
            else:
                print(f"Ihre Eingabe ist nicht innerhalb der Grenzen {lower_limit} und {upper_limit}")
        # Falls ValueError ausgelöst wird der Nutzer gefragt, ob er die Eingabe wiederholen will
        except ValueError:
            print(f"Ihre Eingabe entspricht nicht dem Datentyp {data_type}")
        retry = input("Wollen sie es erneut versuchen (J/n): ")
        # Abbruchbedingung
        if retry.lower() == 'n':
            raise ValueError

def save_data(folgen_glieder: list, *parameter) -> PathLike:
    """
    Speichern von Folgengliedern und Eingabeparametern
    von M. van Straten und P. Merz
    params: folgen_glieder - Liste mit Folgengliedern als Elementen
            *parameter - Beliebige Anzahl an Parametern
    returns: Pfad als Pathlike zur gespeicherten Datei
    """
    data = dict()
    # Folgenglieder und parameter werden im Dictionary eingespeichert
    data["folgen_glieder"] = folgen_glieder
    data["parameter"] = parameter
    # Das Dictionary data wird in die Datei save.json eingespeichert
    json.dump(data, open("save.json", mode="w"))

def load_data(pfad: PathLike) -> tuple:
    """
    Laden von Dateien
    von M. van Straten und P. Merz
    params: pfad - Dateipfad von der Datei die geladen werden soll
    returns: Daten die aus der Datei geladen wurden
    """
    data = json.load(open(pfad))
    return data["folgen_glieder"], data["parameter"]

def main():
    # Beispiel zur Verwendung von read_number
    anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein. "
    eingabe_zahl = read_number(anfrage, int, 3.0, 7.0)
    # Beispiel zur Verwendung von save_data
    save_data([1, 2, 3], 4, 3, 4)
    #Beispiel zur Verwendung von read_data
    folgen_glieder, (param_a, param_b, param_c) = load_data("save.json")
    print(folgen_glieder, param_a, param_b, param_c,)
    
if __name__ == "__main__":
    main()
