import csv
from datetime import date
from pathlib import Path

SNAPSHOT_DATE = date.today().isoformat()
SILVER_PATH = (
    Path("data/silver/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
    / "weather.csv"
)
GOLD_PATH = (
    Path("data/gold/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
    / "weather.csv"
)


def load_silver_rows(path):
    with open(path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file, delimiter=";"))


def add_gold_indicators(rows):
    gold_rows = []

    for row in rows:
        temperature_max = float(row["temperature_max_c"])
        temperature_min = float(row["temperature_min_c"])
        precipitation = float(row["precipitation_mm"])

        gold_rows.append(
            {
                **row,
                "temperature_range_c": round(temperature_max - temperature_min, 2),
                "has_rain": precipitation > 0,
            }
        )

    return gold_rows


def save_gold_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "snapshot_date",
                "forecast_date",
                "city_id",
                "city_name",
                "state",
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
    silver_rows = load_silver_rows(SILVER_PATH)
    gold_rows = add_gold_indicators(silver_rows)
    save_gold_csv(gold_rows, GOLD_PATH)

    print(f"Arquivo salvo em: {GOLD_PATH}")
    print(f"Linhas geradas: {len(gold_rows)}")


if __name__ == "__main__":
    main()