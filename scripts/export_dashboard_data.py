import sqlite3
from pathlib import Path

import pandas as pd


def export_dashboard_data():
    database_path = Path("data/weather_data.db")
    dashboard_folder = Path("dashboard")

    summary_output_file = dashboard_folder / "exported_analysis.csv"
    hourly_output_file = dashboard_folder / "hourly_weather_data.csv"

    dashboard_folder.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)

    summary_query = """
    SELECT
        city,
        ROUND(AVG(temperature_2m), 2) AS avg_temperature,
        ROUND(AVG(relative_humidity_2m), 2) AS avg_humidity,
        MAX(temperature_2m) AS max_temperature,
        MIN(temperature_2m) AS min_temperature,
        COUNT(*) AS total_records
    FROM weather_data
    GROUP BY city
    ORDER BY avg_temperature DESC;
    """

    hourly_query = """
    SELECT
        city,
        latitude,
        longitude,
        time,
        temperature_2m,
        relative_humidity_2m,
        extracted_at
    FROM weather_data
    ORDER BY city, time;
    """

    summary_df = pd.read_sql_query(summary_query, connection)
    hourly_df = pd.read_sql_query(hourly_query, connection)

    summary_df.to_csv(summary_output_file, index=False)
    hourly_df.to_csv(hourly_output_file, index=False)

    connection.close()

    print("Dashboard data exported successfully!")
    print(f"Summary file saved to: {summary_output_file}")
    print(f"Hourly file saved to: {hourly_output_file}")
    print(f"Summary rows: {len(summary_df)}")
    print(f"Hourly rows: {len(hourly_df)}")


if __name__ == "__main__":
    export_dashboard_data()