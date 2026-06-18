import csv
from pathlib import Path


SILVER_PATH = Path("data/silver/weather_cuiaba.csv")
GOLD_PATH = Path("data/gold/weather_cuiaba_summary.csv")


def main():
    rows = []

    with open(SILVER_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            temperature_max = float(row["temperature_max_c"])
            temperature_min = float(row["temperature_min_c"])
            precipitation = float(row["precipitation_mm"])

            row["temperature_range_c"] = round(temperature_max - temperature_min, 2)
            row["has_rain"] = precipitation > 0

            rows.append(row)

    GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(GOLD_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date",
                "city",
                "temperature_max_c",
                "temperature_min_c",
                "precipitation_mm",
                "temperature_range_c",
                "has_rain",
            ],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Arquivo salvo em: {GOLD_PATH}")


if __name__ == "__main__":
    main()