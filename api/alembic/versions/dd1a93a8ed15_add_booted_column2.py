"""add booted column2

Revision ID: dd1a93a8ed15
Revises: ba51fb312d0a
Create Date: 2024-10-10 14:13:31.762915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd1a93a8ed15'
down_revision: Union[str, None] = 'ba51fb312d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
