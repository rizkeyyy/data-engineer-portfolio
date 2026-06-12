import sqlite3
import pandas as pd
from pathlib import Path

def load_weather_data():
    csv_path = Path("data/processed/clean_weather_data.csv")
    database_path = Path("data/weather_data.db")

    if not csv_path.exists():
        print("file tidak ada")
        return

    df = pd.read_csv(csv_path)

    connection = sqlite3.connect(database_path)

    df.to_sql(
        "weather_data",
        connection,
        if_exists="replace",
        index=False
    )

    total_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS total_rows FROM weather_data",
        connection
    )

    print("Data berhasil dimasukkan ke database.")
    print(f"Lokasi database: {database_path}")
    print(total_rows)

    connection.close()


if __name__ == "__main__":
    load_weather_data()