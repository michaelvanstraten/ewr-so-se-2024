import json
from os import PathLike 

def read_number(question: str, data_type: type, lower_limit: float = float("-Inf"), upper_limit: float = float("Inf")) -> "data_type":

    while True:
        answer = input(question)
        try:       
            input_value = data_type(answer)
            if lower_limit <= input_value <= upper_limit:
                return input_value                 
            else:
                print(f"Ihre Eingabe ist nicht innerhalb der Grenzen {lower_limit} und {upper_limit}")
        except ValueError:
            print(f"Ihre Eingabe entspricht nicht dem Datentyp {data_type}")
    
        retry = input("Wollen sie es erneut versuchen (J/n): ")
        if retry.lower() == 'n':
            raise ValueError

# anfrage = "Bitte geben Sie eine ganze Zahl x mit 3 <= x <= 7 ein."
# eingabe_zahl = read_number(anfrage, int, 3.0, 7.0)

def save_data(folgen_glieder: list, *parameter) -> PathLike:
    data = dict()
    data["folgen_glieder"] = folgen_glieder
    data["parameter"] = parameter
    json.dump(data, open("save.json", mode="w"))    

# save_data([1, 2, 3], 4, 3, 4)


def load_data(pfad: PathLike) -> tuple:
    data = json.load(open(pfad))
    return data["folgen_glieder"], data["parameter"]

folgen_glieder, (a, b, c) = load_data("save.json")
print(folgen_glieder, a, b, c, rest)
      
        
