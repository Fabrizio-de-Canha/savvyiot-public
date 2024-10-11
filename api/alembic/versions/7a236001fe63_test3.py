"""test3

Revision ID: 7a236001fe63
Revises: c632289b425e
Create Date: 2024-10-10 14:33:16.575523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a236001fe63'
down_revision: Union[str, None] = 'c632289b425e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
