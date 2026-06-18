import csv
import json
from pathlib import Path


BRONZE_PATH = Path("data/bronze/weather_cuiaba.json")
SILVER_PATH = Path("data/silver/weather_cuiaba.csv")


def main():
    with open(BRONZE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

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

    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(SILVER_PATH, "w", newline="", encoding="utf-8") as file:
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

    print(f"Arquivo salvo em: {SILVER_PATH}")


if __name__ == "__main__":
    main()