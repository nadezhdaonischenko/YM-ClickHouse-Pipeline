"""
Конфигурация проекта.

Все настройки загружаются из файла .env.
"""

from pathlib import Path

import os

from dotenv import load_dotenv


# Пути проекта

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ClickHouse

CLICKHOUSE_HOST = os.getenv(
    "CLICKHOUSE_HOST",
    "localhost",
)

CLICKHOUSE_PORT = int(
    os.getenv(
        "CLICKHOUSE_PORT",
        "8123",
    )
)

CLICKHOUSE_DATABASE = os.getenv(
    "CLICKHOUSE_DATABASE",
    "metrika",
)

CLICKHOUSE_USER = os.getenv(
    "CLICKHOUSE_USER",
    "default",
)

CLICKHOUSE_PASSWORD = os.getenv(
    "CLICKHOUSE_PASSWORD",
    "",
)

CLICKHOUSE_URL = (
    f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}"
)


# Яндекс Метрика

YANDEX_METRIKA_HOST = os.getenv(
    "YANDEX_METRIKA_HOST",
    "https://api-metrika.yandex.net",
)

YANDEX_METRIKA_TOKEN = os.getenv(
    "YANDEX_METRIKA_TOKEN",
    "",
)


# Retry API

API_MAX_RETRIES = int(
    os.getenv("API_MAX_RETRIES", 5)
)

API_RETRY_DELAY = int(
    os.getenv("API_RETRY_DELAY", 3)
)

HTTP_TIMEOUT = int(
    os.getenv("HTTP_TIMEOUT", 60)
)


# Формат даты

DATE_FORMAT = os.getenv(
    "DATE_FORMAT",
    "%Y-%m-%d",
)


# Logs API

COUNTER_ID = int(
    os.getenv("COUNTER_ID", "0")
)

START_DATE = os.getenv("START_DATE")

END_DATE = os.getenv("END_DATE")

SOURCE = os.getenv(
    "SOURCE",
    "visits",
)


# ETL

POLL_INTERVAL = int(
    os.getenv("POLL_INTERVAL", "5")
)

MAX_WAIT_TIME = int(
    os.getenv("MAX_WAIT_TIME", "1800")
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "10000")
)


# Logging

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)