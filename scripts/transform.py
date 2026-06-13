import json
import pandas as pd
from pathlib import Path

def transform_weather_data():
    raw_folder = Path("data/raw")
    processed_folder = Path("data/processed")
    processed_folder.mkdir(parents=True, exist_ok=True)

    all_weather_data = []

    json_files = list(raw_folder.glob("*.json"))

    for json_file in json_files:
        with open(json_file, "r") as file:
            data = json.load(file)

        city = data["city"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        extracted_at = data["extracted_at"]

        hourly_data = data["weather"]["hourly"]

        times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]
        humidities = hourly_data["relative_humidity_2m"]

        for i in range(len(times)):
            row = {
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
                "time": times[i],
                "temperature_2m": temperatures[i],
                "relative_humidity_2m": humidities[i],
                "extracted_at": extracted_at
            }

            all_weather_data.append(row)

    df = pd.DataFrame(all_weather_data)

    before_dedup = len(df)

    df["extracted_at"] = pd.to_datetime(df["extracted_at"])

    df = df.sort_values("extracted_at")

    df = df.drop_duplicates(
        subset=["city", "time"],
        keep="last"
    )

    after_dedup = len(df)

    output_path = processed_folder / "clean_weather_data.csv"
    df.to_csv(output_path, index=False)

    print(f"Jumlah data sebelum deduplication: {before_dedup}")
    print(f"Jumlah data setelah deduplication: {after_dedup}")
    print(f"Jumlah duplicate yang dihapus: {before_dedup - after_dedup}")

if __name__ == "__main__":
    transform_weather_data()