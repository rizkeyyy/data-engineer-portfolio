import pandas as pd
from pathlib import Path

def check_data_quality():
    file_path = Path("data/processed/clean_weather_data.csv")

    if not file_path.exists():
        print("File tidak ada")
        return

    df = pd.read_csv(file_path)

    print("Jumlah baris dan kolom: ")
    print(df.shape)

    print("\n5 data teratas: ")
    print(df.head())

    print("\nTipe data teratas: ")
    print(df.dtypes)

    print("\nJumlah data kosong per kolom: ")
    print(df.isnull().sum())

    print("\nJumlah data duplicate: ")
    print(df.duplicated().sum())

    print("\nRata-Rata suhu per kota: ")
    print(df.groupby('city')['temperature_2m'].mean())

    print("\nRata-Rata kelembaban per kota: ")
    print(df.groupby("city")["temperature_2m"].mean().sort_values(ascending=False))

if __name__ == "__main__":
    check_data_quality()