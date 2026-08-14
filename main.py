"""
Точка входа ETL.

Загрузка данных из Яндекс Метрики
в ClickHouse.
"""

from __future__ import annotations
from api.models import LogsRequest
from config.schema import VISIT_FIELDS
from config import settings
from services.etl import run_etl


def main() -> None:
    """
    Запускает ETL.
    """

    request = LogsRequest(
        counter_id=settings.COUNTER_ID,
        token=settings.YANDEX_METRIKA_TOKEN,
        start_date=settings.START_DATE,
        end_date=settings.END_DATE,
        source=settings.SOURCE,
        fields=VISIT_FIELDS,
    )

    run_etl(request)


if __name__ == "__main__":
    main()