"""
Работа с ClickHouse.

Содержит функции:

- подключение к базе;
- выполнение SQL-запросов;
- загрузка DataFrame;
"""

import clickhouse_connect

from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


def database_connect():
    """
    Создает подключение к ClickHouse.
    """

    try:
        client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DATABASE,
        )

        logger.info(
            "Connected to ClickHouse: http://%s:%s",
            settings.CLICKHOUSE_HOST,
            settings.CLICKHOUSE_PORT,
        )

        return client

    except Exception:
        logger.exception(
            "Failed to connect to ClickHouse."
        )
        raise


def execute(client, sql: str):
    """
    Выполняет SQL-запрос.
    """

    logger.debug("SQL: %s", sql)

    try:
        return client.command(sql)

    except Exception:
        logger.exception(
            "SQL execution failed."
        )
        raise


def insert_dataframe(
    client,
    df,
    table: str = "visit",
) -> None:
    """
    Загружает DataFrame в ClickHouse.
    """

    if df.empty:
        logger.warning(
            "Nothing to insert."
        )
        return

    try:
        client.insert_df(
            table=table,
            df=df,
            database=settings.CLICKHOUSE_DATABASE,
        )

        logger.info(
            "Inserted %s rows.",
            len(df),
        )

    except Exception:
        logger.exception(
            "Insert failed."
        )
        raise


def get_visit_stats(client) -> dict:
    """
    Возвращает статистику по загруженным визитам.
    """

    sql = """
        SELECT
            count() AS total_rows,
            uniqExact(counter_id, visit_id) AS unique_visits
        FROM metrika.visit FINAL
    """

    result = client.query(sql)

    row = result.result_rows[0]

    total_rows = row[0]
    unique_visits = row[1]
    duplicates = total_rows - unique_visits

    return {
        "total_rows": total_rows,
        "unique_visits": unique_visits,
        "duplicates": duplicates,
    }