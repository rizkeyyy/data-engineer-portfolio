import requests
import json
from datetime import datetime
from pathlib import Path


CITIES = [
    {"city": "Jakarta", "latitude": -6.2088, "longitude": 106.8456},
    {"city": "Bandung", "latitude": -6.9175, "longitude": 107.6191},
    {"city": "Surabaya", "latitude": -7.2575, "longitude": 112.7521},
    {"city": "Medan", "latitude": 3.5952, "longitude": 98.6722},
    {"city": "Makassar", "latitude": -5.1477, "longitude": 119.4327},
]


def extract_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"

    raw_folder = Path("data/raw")
    raw_folder.mkdir(parents=True, exist_ok=True)

    for city in CITIES:
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "Asia/Jakarta"
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        weather_data = response.json()

        final_data = {
            "city": city["city"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weather": weather_data
        }

        file_name = f"weather_{city['city'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = raw_folder / file_name

        with open(file_path, "w") as file:
            json.dump(final_data, file, indent=4)

        print(f"Data {city['city']} berhasil disimpan ke: {file_path}")


if __name__ == "__main__":
    extract_weather_data()