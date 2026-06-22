import csv
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

CAPITALS_PATH = Path("config/capitals.csv")
BRONZE_DIR = Path("data/bronze/capital_forecasts")
SNAPSHOT_DATE = date.today().isoformat()

def load_capitals(path):
    with open(path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))
    
def build_weather_url(capital):
    parameters = {
        "latitude": capital["latitude"],
        "longitude": capital["longitude"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }

    return "https://api.open-meteo.com/v1/forecast?" + urlencode(parameters)

def fetch_weather_data(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def save_bronze_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main():
    capitals = load_capitals(CAPITALS_PATH)

    for capital in capitals:
        url = build_weather_url(capital)
        data = fetch_weather_data(url)

        bronze_path = (
            BRONZE_DIR
            / f"snapshot_date={SNAPSHOT_DATE}"
            / f"{capital['city_id']}.json"
        )

        save_bronze_json(data, bronze_path)
        print(f"Arquivo salvo para {capital['city_name']}: {bronze_path}")

    print(f"Extracao concluida para {len(capitals)} capitais.")


if __name__ == "__main__":
    main()