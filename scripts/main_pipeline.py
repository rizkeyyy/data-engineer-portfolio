from extract import extract_weather_data
from transform import transform_weather_data
from check_data_quality import check_data_quality
from load import load_weather_data
from run_analysis import run_analysis


def main():
    print("Starting Weather Data ETL Pipeline...\n")

    print("Step 1: Extract data from API")
    extract_weather_data()

    print("\nStep 2: Transform raw JSON into clean CSV")
    transform_weather_data()

    print("\nStep 3: Check data quality")
    check_data_quality()

    print("\nStep 4: Load clean data into SQLite database")
    load_weather_data()

    print("\nStep 5: Run SQL analysis")
    run_analysis()

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()