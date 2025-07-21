import csv
from pathlib import Path
from typing import Tuple


def csv_converter(
    input_file: str = "./data/markets.csv",
    output_file: str = "./data/markets_converted.csv",
    input_format: Tuple[str, str] = (",", ";"),
    output_format: Tuple[str, str] = ("|", ","),
) -> None:
    """
    Convertit un fichier CSV avec un format (séparateur de colonne + séparateur dans les cellules)
    vers un autre format.
    """
    if not all(isinstance(sep, str) and sep for sep in (*input_format, *output_format)):
        raise ValueError("Les séparateurs doivent être des chaînes non vides.")

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {input_path}")

    try:
        with input_path.open("r", encoding="utf-8", newline="") as infile, \
             output_path.open("w", encoding="utf-8", newline="") as outfile:

            reader = csv.reader(infile, delimiter=input_format[0])
            writer = csv.writer(outfile, delimiter=output_format[0], quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                new_row = [cell.replace(input_format[1], output_format[1]) for cell in row]
                writer.writerow(new_row)

        print(f"✅ Conversion réussie : {output_path}")

    except csv.Error as e:
        raise csv.Error(f"Erreur CSV ligne inconnue : {e}")
    except Exception as e:
        raise RuntimeError(f"Erreur inattendue : {e}")


if __name__ == "__main__":
    try:
        csv_converter()
    except Exception as err:
        print(f"❌ Échec de conversion : {err}")