"""add cascades & relationships

Revision ID: fd42a6edc5fa
Revises: 205e9f7b57de
Create Date: 2025-05-08 18:00:16.163593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd42a6edc5fa'
down_revision: Union[str, None] = '205e9f7b57de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
