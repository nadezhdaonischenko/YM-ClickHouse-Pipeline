"""
Конфигурация Alembic для миграций базы данных ClickHouse.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import pool

import clickhouse_connect.cc_sqlalchemy.alembic

from config import settings


# Alembic Config

config = context.config


# Logging

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ClickHouse URL

clickhouse_url = (
    f"clickhousedb+connect://"
    f"{settings.CLICKHOUSE_USER}:"
    f"{settings.CLICKHOUSE_PASSWORD}@"
    f"{settings.CLICKHOUSE_HOST}:"
    f"{settings.CLICKHOUSE_PORT}/"
    f"{settings.CLICKHOUSE_DATABASE}"
)

config.set_main_option(
    "sqlalchemy.url",
    clickhouse_url,
)


# Metadata

target_metadata = None


# Offline migrations

def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# Online migrations

def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Run

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()
