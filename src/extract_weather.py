import json
from pathlib import Path
from urllib.request import urlopen


URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-15.5961"
    "&longitude=-56.0967"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=America/Cuiaba"
)

BRONZE_PATH = Path("data/bronze/weather_cuiaba.json")


def fetch_weather_data(url):
    with urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def save_bronze_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def main():
    data = fetch_weather_data(URL)
    save_bronze_json(data, BRONZE_PATH)

    print(f"Arquivo salvo em: {BRONZE_PATH}")


if __name__ == "__main__":
    main()