"""Инициализация таблицы визитов в ClickHouse.

Revision ID: 41a99f5aeefe
Revises:
"""

from typing import Sequence, Union

from alembic import op


revision: str = "41a99f5aeefe"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Создаёт начальную таблицу визитов.
    """

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS metrika.visit
        (
            visit_id UInt64,
            counter_id UInt32,
            client_id UInt64,

            date Date DEFAULT '1970-01-01',
            date_time DateTime DEFAULT '0000000000',

            start_url String,
            end_url String,

            page_views UInt32,
            visit_duration UInt32,
            is_bounce UInt8,
            new_user UInt8,

            ip_address String,
            network_type String,

            region_country String,
            region_city String,

            traffic_source String,
            search_engine_root String,
            search_engine String,
            referer String,

            utm_source String,
            utm_medium String,
            utm_campaign String,
            utm_content String,
            utm_term String,

            device_category UInt8,

            mobile_phone String,
            mobile_phone_model String,

            operating_system_root String,
            operating_system String,

            browser String,
            browser_major_version UInt16,
            browser_minor_version UInt16,

            cookie_enabled UInt8,
            javascript_enabled UInt8,

            screen_colors UInt8,
            screen_width UInt16,
            screen_height UInt16,
            window_client_width UInt16,
            window_client_height UInt16,

            loaded_at DateTime DEFAULT '0000000000'
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMM(date)
        ORDER BY (date, visit_id)
        """
    )


def downgrade() -> None:
    """
    Удаляет таблицу визитов.
    """

    op.execute(
        """
        DROP TABLE IF EXISTS metrika.visit
        """
    )
