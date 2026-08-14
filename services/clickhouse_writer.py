"""
Загрузка данных в ClickHouse.
"""

from __future__ import annotations

from datetime import datetime
from io import StringIO

import pandas as pd

from config import settings
from config.schema import VISIT_SCHEMA, CLICKHOUSE_COLUMNS
from database.connection import (
    database_connect,
    insert_dataframe,
)
from utils.logger import get_logger


logger = get_logger(__name__)


# Rename columns mapping

RENAME_COLUMNS = {
    field.metrika_name: field.column_name
    for field in VISIT_SCHEMA
}


# Read TSV

def read_tsv(tsv: str) -> pd.DataFrame:
    """
    Преобразует TSV в DataFrame.
    """

    df = pd.read_csv(
        StringIO(tsv),
        sep="\t",
        low_memory=False,
    )

    logger.info(
        "Loaded %s rows from TSV.",
        len(df),
    )

    return df


# Rename columns

def rename_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Переименовывает колонки
    согласно schema.py.
    """

    return df.rename(
        columns=RENAME_COLUMNS,
    )


# Validate columns

def validate_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Проверяет наличие всех столбцов,
    необходимых для загрузки в ClickHouse.

    Если столбца нет — создаёт его.
    """

    missing_columns = []

    for column in CLICKHOUSE_COLUMNS:

        if column not in df.columns:

            df[column] = None

            missing_columns.append(column)

    if missing_columns:

        logger.warning(
            "Added missing columns: %s",
            ", ".join(missing_columns),
        )

    return df


# Normalize values

def normalize_nulls(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Нормализует значения согласно
    типам из VISIT_SCHEMA.
    """

    df = df.copy()

    numeric_types = {
        "UInt8",
        "UInt16",
        "UInt32",
        "UInt64",
        "Int8",
        "Int16",
        "Int32",
        "Int64",
        "Float32",
        "Float64",
    }

    for field in VISIT_SCHEMA:

        column = field.column_name

        if column not in df.columns:
            continue

        if field.clickhouse_type in numeric_types:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            ).fillna(0)

        elif field.clickhouse_type == "String":

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
            )

    return df


# Dates

def normalize_dates(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Приводит даты к формату,
    который принимает ClickHouse.
    """

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        ).dt.date

    if "date_time" in df.columns:

        df["date_time"] = pd.to_datetime(
            df["date_time"],
            errors="coerce",
        )

    return df


# Loaded at

def add_loaded_at(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Добавляет время загрузки и версию записи.
    """

    loaded_at = datetime.now()

    df["loaded_at"] = loaded_at

    df["version"] = int(
        loaded_at.timestamp() * 1000
    )

    return df


# Column order

def prepare_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Оставляет только необходимые колонки
    и приводит их к порядку schema.py.
    """

    columns = [
        field.column_name
        for field in VISIT_SCHEMA
    ]

    columns.append("loaded_at")
    columns.append("version")

    return df[columns]


# Insert

def insert_data(
    df: pd.DataFrame,
) -> None:
    """
    Загружает DataFrame в ClickHouse
    пакетами.
    """

    if df.empty:

        logger.warning(
            "Nothing to insert."
        )

        return

    client = database_connect()

    total_rows = len(df)

    for start in range(
        0,
        total_rows,
        settings.CHUNK_SIZE,
    ):

        end = min(
            start + settings.CHUNK_SIZE,
            total_rows,
        )

        chunk = df.iloc[start:end].copy()

        logger.info(
            "Inserting rows %s-%s of %s.",
            start + 1,
            end,
            total_rows,
        )

        insert_dataframe(
            client,
            chunk,
        )


# Main writer

def write_tsv(
    tsv: str,
) -> None:
    """
    Загружает TSV
    в ClickHouse.
    """

    df = read_tsv(tsv)

    if df.empty:

        logger.warning(
            "TSV contains no rows."
        )

        return

    df = rename_columns(df)

    df = validate_columns(df)

    df = normalize_nulls(df)

    df = normalize_dates(df)

    df = add_loaded_at(df)

    df = prepare_columns(df)

    insert_data(df)