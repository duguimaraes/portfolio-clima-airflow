import csv
import json
from datetime import date
from pathlib import Path

CAPITALS_PATH = Path("config/capitals.csv")
BRONZE_DIR = Path("data/bronze/capital_forecasts")
SNAPSHOT_DATE = date.today().isoformat()
SILVER_PATH = (
    Path("data/silver/capital_forecasts")
    / f"snapshot_date={SNAPSHOT_DATE}"
    / "weather.csv"
)


def load_capitals(path):
    with open(path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_bronze_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_to_rows(capitals):
    rows = []

    for capital in capitals:
        bronze_path = (
            BRONZE_DIR
            / f"snapshot_date={SNAPSHOT_DATE}"
            / f"{capital['city_id']}.json"
        )

        data = load_bronze_data(bronze_path)
        daily = data["daily"]

        for index, forecast_date in enumerate(daily["time"]):
            rows.append(
                {
                    "snapshot_date": SNAPSHOT_DATE,
                    "forecast_date": forecast_date,
                    "city_id": capital["city_id"],
                    "city_name": capital["city_name"],
                    "state": capital["state"],
                    "temperature_max_c": daily["temperature_2m_max"][index],
                    "temperature_min_c": daily["temperature_2m_min"][index],
                    "precipitation_mm": daily["precipitation_sum"][index],
                }
            )

    return rows


def save_silver_csv(rows, path):
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
            ],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    capitals = load_capitals(CAPITALS_PATH)
    rows = transform_to_rows(capitals)
    save_silver_csv(rows, SILVER_PATH)

    print(f"Arquivo salvo em: {SILVER_PATH}")
    print(f"Linhas geradas: {len(rows)}")


if __name__ == "__main__":
    main()