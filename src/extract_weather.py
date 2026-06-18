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


def main():
    with urlopen(URL) as response:
        data = json.loads(response.read().decode("utf-8"))

    output_path = Path("data/bronze/weather_cuiaba.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Arquivo salvo em: {output_path}")


if __name__ == "__main__":
    main()