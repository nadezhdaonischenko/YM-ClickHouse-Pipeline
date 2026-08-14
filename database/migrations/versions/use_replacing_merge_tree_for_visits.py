"""Подготовка таблицы к использованию ReplacingMergeTree.

Revision ID: a8528fefed04
Revises: 41a99f5aeefe

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8528fefed04'
down_revision: Union[str, Sequence[str], None] = '41a99f5aeefe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Подготавливает таблицу к использованию
    ReplacingMergeTree.

    Добавляем версию записи.
    """

    op.execute(
        """
        ALTER TABLE metrika.visit
        ADD COLUMN IF NOT EXISTS version UInt64
        DEFAULT toUnixTimestamp64Milli(now64())
        """
    )


def downgrade() -> None:
    """
    Удаляет колонку версии.
    """

    op.execute(
        """
        ALTER TABLE metrika.visit
        DROP COLUMN IF EXISTS version
        """
    )
