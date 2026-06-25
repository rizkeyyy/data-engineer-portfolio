# Indonesia Weather Data ETL Pipeline

> **Data Engineering Portfolio Project** — End-to-end ETL pipeline yang mengumpulkan data cuaca dari 5 kota besar Indonesia secara otomatis, lalu memprosesnya untuk analisis.

---

## Overview

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
| **Apache Airflow 3.x** | Pipeline orchestration & scheduling |
| **LocalExecutor** | Task executor — jalankan task langsung di scheduler process |
| **PostgreSQL** | Airflow metadata database (via Docker) |
| **Docker & Docker Compose** | Containerized deployment Airflow |
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

## Pipeline Berjalan

ETL pipeline berhasil di-orkestrasi menggunakan Apache Airflow dengan Docker dan LocalExecutor.

![Airflow Success](assets/airflow%20sukses.png)

Urutan task pipeline:

1. **Extract** — Ambil data cuaca dari Open-Meteo API untuk 5 kota besar Indonesia
2. **Transform** — Konversi raw JSON menjadi data tabular bersih dalam format CSV (flatten + deduplication)
3. **Quality Check** — Validasi data: null check, duplicate check, shape check
4. **Load** — Masukkan data bersih ke dalam database SQLite
5. **Analysis** — Jalankan SQL query untuk rata-rata/maks/min suhu & kelembaban per kota

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

### 1. Clone Repository

```bash
git clone https://github.com/rizkeyyy/data-engineer-portfolio.git
cd data-engineer-portfolio
```

### 2. Jalankan Pipeline Manual (tanpa Airflow)

Setup environment dulu:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Lalu jalankan pipeline:

```bash
cd scripts
python main_pipeline.py
```

Ini akan menjalankan semua 5 step secara berurutan.

### 3. Jalankan Per Step

```bash
cd scripts

python extract.py             # Step 1: Ambil data dari API
python transform.py           # Step 2: Transform JSON → CSV
python check_data_quality.py  # Step 3: Cek kualitas data
python load.py                # Step 4: Load ke SQLite
python run_analysis.py        # Step 5: Analisis hasil
```

### 4. Jalankan dengan Apache Airflow (Docker Compose)

Project ini menggunakan **Docker Compose** dengan **LocalExecutor** untuk menjalankan Airflow secara lokal.

> **Kenapa LocalExecutor?**  
> Sebelumnya pakai CeleryExecutor, tapi muncul masalah: task terus-terusan `queued`, `airflow-worker` unhealthy, dan worker timeout. LocalExecutor lebih ringan dan cocok untuk development environment — task langsung dieksekusi oleh scheduler tanpa perlu Redis broker atau worker terpisah.

**Prerequisites:** Docker Desktop harus sudah terinstall dan berjalan.

```bash
# Buat file .env (isi FERNET_KEY & JWT secret)
echo "AIRFLOW_UID=50000" > .env
echo "FERNET_KEY=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env

# Jalankan semua service
docker compose up -d
```

Tunggu sampai semua container healthy, lalu buka:
- **Airflow UI** → `http://localhost:8080`
- Login: `airflow` / `airflow`
- Cari DAG `weather_etl_pipeline`, lalu aktifkan.

**Services yang berjalan:**

| Service | Keterangan |
|---------|------------|
| `postgres` | Metadata database Airflow |
| `airflow-apiserver` | REST API & UI (port 8080) |
| `airflow-scheduler` | Scheduling + eksekusi task (LocalExecutor) |
| `airflow-dag-processor` | Parse & register DAG files |
| `airflow-triggerer` | Handle deferred tasks |

```bash
# Cek status semua container
docker compose ps

# Lihat logs
docker compose logs -f airflow-scheduler

# Matikan semua service
docker compose down
```

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

- [x] Containerize pipeline dengan **Docker Compose**
- [x] Migrasi executor ke **LocalExecutor** (fix: task queued, worker unhealthy)
- [ ] Migrasi database dari SQLite ke **PostgreSQL** (untuk pipeline data, bukan hanya Airflow metadata)
- [ ] Tambah visualisasi data di **Jupyter Notebook**
- [ ] Export hasil analisis ke **Google Sheets / BigQuery**
- [ ] Tambah **alerting** jika pipeline gagal (email/Slack)
- [ ] Tambah lebih banyak kota & metrics cuaca

---

## 👤 Author

**Rizki** — Data Engineer in progress  
🔗 GitHub: [@rizkeyyy](https://github.com/rizkeyyy)
