# Indonesia Weather Data ETL Pipeline

> **Data Engineering Portfolio Project** — End-to-end ETL pipeline yang mengumpulkan data cuaca dari 5 kota besar Indonesia secara otomatis, lalu memprosesnya untuk analisis.

---

## 📌 Overview

Project ini adalah implementasi nyata dari sebuah **ETL (Extract, Transform, Load) pipeline** yang:

1. **Extract** — Menarik data cuaca secara real-time dari [Open-Meteo API](https://open-meteo.com/) (free, no API key needed)
2. **Transform** — Membersihkan & menggabungkan data JSON menjadi format CSV yang terstruktur, termasuk proses deduplication
3. **Quality Check** — Memvalidasi data sebelum dimasukkan ke database (null check, duplicate check, shape check)
4. **Load** — Menyimpan data bersih ke SQLite database
5. **Analyze** — Menjalankan SQL query untuk insight cuaca per kota
6. **Orchestrate** — Seluruh pipeline dijadwalkan otomatis menggunakan Apache Airflow (daily schedule)

---

## Cities Covered

| Kota | Latitude | Longitude |
|------|----------|-----------|
| Jakarta | -6.2088 | 106.8456 |
| Bandung | -6.9175 | 107.6191 |
| Surabaya | -7.2575 | 112.7521 |
| Medan | 3.5952 | 98.6722 |
| Makassar | -5.1477 | 119.4327 |

---

## Tech Stack

| Tool | Kegunaan |
|------|----------|
| **Python 3.x** | Core scripting & pipeline logic |
| **Pandas** | Data transformation & deduplication |
| **Requests** | HTTP call ke Open-Meteo API |
| **SQLite** | Local database storage |
| **Apache Airflow** | Pipeline orchestration & scheduling |
| **SQL** | Data analysis queries |
| **GitHub** | Version control & portfolio hosting |

---

## Project Structure

```
Data Engineer-portfolio/
│
├── dags/
│   └── weather_etl_dag.py        # Airflow DAG — orchestrates full pipeline (daily)
│
├── scripts/
│   ├── extract.py                # Fetch data dari Open-Meteo API → simpan ke data/raw/
│   ├── transform.py              # Parse JSON, flatten data, deduplication → CSV
│   ├── check_data_quality.py     # Validasi data: null, duplicate, shape, stats per kota
│   ├── load.py                   # Load CSV ke SQLite database
│   ├── run_analysis.py           # Query SQLite → tampilkan analisis per kota
│   └── main_pipeline.py          # Jalankan semua step secara manual (tanpa Airflow)
│
├── sql/
│   └── analysis.sql              # Kumpulan SQL query untuk eksplorasi data
│
├── data/
│   ├── raw/                      # JSON hasil extract per kota (timestamped)
│   ├── processed/                # clean_weather_data.csv hasil transform
│   └── weather_data.db           # SQLite database hasil load
│
├── notebooks/                    # (Planned) EDA & visualisasi
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Pipeline Flow

```
Open-Meteo API
     │
     ▼
[1] extract.py          → data/raw/weather_<city>_<timestamp>.json
     │
     ▼
[2] transform.py        → data/processed/clean_weather_data.csv
     │                    (flatten JSON + deduplication by city+time)
     ▼
[3] check_data_quality.py → validasi null, duplicate, stats
     │
     ▼
[4] load.py             → data/weather_data.db (SQLite table: weather_data)
     │
     ▼
[5] run_analysis.py     → avg/max/min temperature & humidity per kota
```

**Airflow DAG** (`weather_etl_dag.py`) menjalankan semua step di atas secara otomatis setiap hari (`@daily`), dengan dependency chain:

```
extract >> transform >> quality_check >> load >> analysis
```

---

## Data Schema

Tabel `weather_data` di SQLite:

| Column | Type | Keterangan |
|--------|------|-----------|
| `city` | TEXT | Nama kota |
| `latitude` | FLOAT | Koordinat lintang |
| `longitude` | FLOAT | Koordinat bujur |
| `time` | TEXT | Timestamp per jam |
| `temperature_2m` | FLOAT | Suhu udara di ketinggian 2m (°C) |
| `relative_humidity_2m` | FLOAT | Kelembaban relatif (%) |
| `extracted_at` | DATETIME | Waktu data di-extract |

---

## SQL Analysis (`sql/analysis.sql`)

Query yang tersedia untuk eksplorasi data:

1. Preview 10 data pertama
2. Hitung total baris data
3. Rata-rata suhu per kota
4. Rata-rata kelembaban per kota
5. Suhu tertinggi per kota
6. Suhu terendah per kota

---

## How to Run

### 1. Clone & Setup Environment

```bash
git clone https://github.com/rizkeyyy/data-engineer-portfolio.git
cd data-engineer-portfolio

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 2. Jalankan Pipeline Manual (tanpa Airflow)

```bash
cd scripts
python main_pipeline.py
```

Ini akan menjalankan semua 5 step secara berurutan.

### 3. Jalankan Per Step

```bash
cd scripts

python extract.py           # Step 1: Ambil data dari API
python transform.py         # Step 2: Transform JSON → CSV
python check_data_quality.py  # Step 3: Cek kualitas data
python load.py              # Step 4: Load ke SQLite
python run_analysis.py      # Step 5: Analisis hasil
```

### 4. Jalankan dengan Apache Airflow

```bash
# Set Airflow home (opsional)
export AIRFLOW_HOME=$(pwd)

# Init database Airflow (sekali saja)
airflow db init

# Jalankan Airflow webserver & scheduler
airflow webserver --port 8080
airflow scheduler
```

Buka browser ke `http://localhost:8080`, cari DAG `weather_etl_pipeline`, lalu aktifkan.

---

## Key Learnings

- Implementasi **ETL pipeline** end-to-end dari API hingga database
- Penggunaan **Pandas** untuk flatten nested JSON dan deduplication
- **Data Quality Check** sebelum loading ke database
- **Apache Airflow** untuk scheduling & orchestration pipeline
- Penyimpanan data terstruktur dengan **SQLite**
- Analisis data menggunakan **SQL queries**

---

## Roadmap

- [ ] Migrasi database dari SQLite ke **PostgreSQL**
- [ ] Tambah visualisasi data di **Jupyter Notebook**
- [ ] Export hasil analisis ke **Google BigQuery**
- [ ] Containerize pipeline dengan **Docker**
- [ ] Tambah **alerting** jika pipeline gagal (email/Slack)
- [ ] Tambah lebih banyak kota & metrics cuaca

---

## 👤 Author

**Rizki** — Data Engineer in progress  
🔗 GitHub: [@rizkeyyy](https://github.com/rizkeyyy)