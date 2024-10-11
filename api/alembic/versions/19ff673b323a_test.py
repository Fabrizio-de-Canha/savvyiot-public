"""test

Revision ID: 19ff673b323a
Revises: dd1a93a8ed15
Create Date: 2024-10-10 14:15:50.725424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19ff673b323a'
down_revision: Union[str, None] = 'dd1a93a8ed15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
