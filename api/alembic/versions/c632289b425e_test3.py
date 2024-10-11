"""test3

Revision ID: c632289b425e
Revises: 156ed7f5ad6a
Create Date: 2024-10-10 14:28:53.166377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c632289b425e'
down_revision: Union[str, None] = '156ed7f5ad6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
