"""test2

Revision ID: cf8e49b6a227
Revises: 19ff673b323a
Create Date: 2024-10-10 14:19:43.441922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf8e49b6a227'
down_revision: Union[str, None] = '19ff673b323a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
