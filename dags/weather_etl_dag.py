from datetime import datetime

from airflow.decorators import dag, task

from scripts.extract import extract_weather_data
from scripts.transform import transform_weather_data
from scripts.check_data_quality import check_data_quality
from scripts.load import load_weather_data
from scripts.run_analysis import run_analysis


@dag(
    dag_id="weather_etl_pipeline",
    strat_date=datetime(2026, 6, 1),
    schedule="@daily",
    catchup=False,
    tags=["data-engineering", "weather", "portfolio"],
)

def weather_etl_pipeline():

    @task
    def extract_task():
        extract_weather_data()

    @task
    def transform_task():
        transform_weather_data()

    @task
    def quality_check_task():
        check_data_quality()

    @task
    def load_task():
        load_weather_data()

    @task
    def analysis_task():
        run_analysis()

    extract = extract_task()
    transform = transform_task()
    quality_check = quality_check_task()
    load = load_task()
    analysis = analysis_task()

    extract >> transform >> quality_check >> load >> analysis

weather_etl_pipeline()