"""Создание представления текущих визитов в ClickHouse.

Revision ID: 17f416d3c3fa
Revises: 8546c4efb004

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '17f416d3c3fa'
down_revision: Union[str, Sequence[str], None] = '8546c4efb004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create current visits view."""

    op.execute("""
        CREATE VIEW metrika.visit_current AS
        SELECT *
        FROM metrika.visit
        FINAL
    """)


def downgrade() -> None:
    """Drop current visits view."""

    op.execute("""
        DROP VIEW IF EXISTS metrika.visit_current
    """)
