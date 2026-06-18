import csv
from pathlib import Path


SILVER_PATH = Path("data/silver/weather_cuiaba.csv")
GOLD_PATH = Path("data/gold/weather_cuiaba_summary.csv")


def load_silver_rows(path):
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def add_gold_indicators(rows):
    enriched_rows = []

    for row in rows:
        temperature_max = float(row["temperature_max_c"])
        temperature_min = float(row["temperature_min_c"])
        precipitation = float(row["precipitation_mm"])

        row["temperature_range_c"] = round(temperature_max - temperature_min, 2)
        row["has_rain"] = precipitation > 0

        enriched_rows.append(row)

    return enriched_rows


def save_gold_csv(rows, path):
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
                "temperature_range_c",
                "has_rain",
            ],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = load_silver_rows(SILVER_PATH)
    gold_rows = add_gold_indicators(rows)
    save_gold_csv(gold_rows, GOLD_PATH)

    print(f"Arquivo salvo em: {GOLD_PATH}")


if __name__ == "__main__":
    main()