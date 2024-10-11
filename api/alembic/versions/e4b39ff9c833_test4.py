"""test4

Revision ID: e4b39ff9c833
Revises: 7a236001fe63
Create Date: 2024-10-10 14:33:45.625073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4b39ff9c833'
down_revision: Union[str, None] = '7a236001fe63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
