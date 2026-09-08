"""migração

Revision ID: b4dce058177c
Revises: d2c94dd45e6a
Create Date: 2026-09-08 15:07:01.690563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4dce058177c'
down_revision: Union[str, Sequence[str], None] = 'd2c94dd45e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
