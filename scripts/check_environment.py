import pandas as pd
import requests

print("Data ready!")

sample_data = {
    "city": ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar", "Yogyakarta", "Semarang", "Denpasar"],
    "temperature": [31, 24, 33, 30, 32, 28, 29, 31],
    "humidity": [70, 80, 65, 75, 68, 77, 72, 69]
}

df = pd.DataFrame(sample_data)

print(df)
