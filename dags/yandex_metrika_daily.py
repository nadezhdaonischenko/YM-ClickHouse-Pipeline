from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context

from api.models import LogsRequest
from config import settings
from config.schema import VISIT_FIELDS
from services.etl import run_etl


def run_daily_etl():
    context = get_current_context()
    
    logical_date = context["logical_date"]

    target_date = (logical_date - timedelta(days=1)).strftime("%Y-%m-%d")

    request = LogsRequest(
        counter_id=settings.COUNTER_ID,
        token=settings.YANDEX_METRIKA_TOKEN,
        start_date=target_date,
        end_date=target_date,
        source=settings.SOURCE,
        fields=VISIT_FIELDS,
    )

    run_etl(request)


with DAG(
    dag_id="yandex_metrika_daily",
    start_date=datetime(2026, 8, 11),
    schedule="0 6 * * *",
    catchup=True,
    tags=["yandex", "metrika", "clickhouse", "etl"],
) as dag:

    load_metrika = PythonOperator(
        task_id="load_metrika",
        python_callable=run_daily_etl,
    )