import csv
import json
from pathlib import Path


BRONZE_PATH = Path("data/bronze/weather_cuiaba.json")
SILVER_PATH = Path("data/silver/weather_cuiaba.csv")


def load_bronze_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_to_rows(data):
    daily = data["daily"]
    rows = []

    for index, date in enumerate(daily["time"]):
        row = {
            "date": date,
            "city": "Cuiaba",
            "temperature_max_c": daily["temperature_2m_max"][index],
            "temperature_min_c": daily["temperature_2m_min"][index],
            "precipitation_mm": daily["precipitation_sum"][index],
        }

        rows.append(row)

    return rows


def save_silver_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date",
                "city",
                "temperature_max_c",
                "temperature_min_c",
                "precipitation_mm",
            ],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    data = load_bronze_data(BRONZE_PATH)
    rows = transform_to_rows(data)
    save_silver_csv(rows, SILVER_PATH)

    print(f"Arquivo salvo em: {SILVER_PATH}")


if __name__ == "__main__":
    main()