import sqlite3
import pandas as pd
from pathlib import Path


def run_analysis():
    database_path = Path("data/weather_data.db")

    if not database_path.exists():
        print("Database belum ditemukan. Jalankan scripts/load.py dulu.")
        return

    connection = sqlite3.connect(database_path)

    query = """
    SELECT 
        city,
        ROUND(AVG(temperature_2m), 2) AS avg_temperature,
        ROUND(AVG(relative_humidity_2m), 2) AS avg_humidity,
        MAX(temperature_2m) AS max_temperature,
        MIN(temperature_2m) AS min_temperature
    FROM weather_data
    GROUP BY city
    ORDER BY avg_temperature DESC;
    """

    result = pd.read_sql_query(query, connection)

    print("Hasil analisis cuaca per kota:")
    print(result)

    connection.close()


if __name__ == "__main__":
    run_analysis()