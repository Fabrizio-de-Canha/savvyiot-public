"""test5

Revision ID: 3064eae55dd4
Revises: e4b39ff9c833
Create Date: 2024-10-10 14:37:56.317627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3064eae55dd4'
down_revision: Union[str, None] = 'e4b39ff9c833'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
