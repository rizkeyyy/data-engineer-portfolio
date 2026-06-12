-- 1. cek 10 data pertama
SELECT *
FROM weather_data
LIMIT 10;

-- 2. Hitung total data
SELECT COUNT(*) AS total_rows
FROM weather_data;

-- 3. Rata-rata suhu per kota
SELECT
    city,
    ROUND(AVG(temperature_2m),2) AS avg_temperature
FROM weather_data
GROUP BY city
ORDER BY avg_temperature DESC;

-- 4. Rata-rata kelembapan per kota
SELECT
    city,
    ROUND(AVG(relative_humidity_2m),2) AS avg_humidity
FROM weather_data
GROUP BY city
ORDER BY avg_humidity DESC;

-- 5. Suhu tertinggi per kota
SELECT
    city,
    MAX(temperature_2m) AS max_temperature
GROUP BY city
ORDER BY max_temperature DESC;

-- 6. Suhu terendah per kota
SELECT 
    city,
    MIN(temperature_2m) AS min_temperature
FROM weather_data
GROUP BY city
ORDER BY min_temperature ASC;
