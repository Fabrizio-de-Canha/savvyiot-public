"""test2

Revision ID: 156ed7f5ad6a
Revises: cf8e49b6a227
Create Date: 2024-10-10 14:23:42.852464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '156ed7f5ad6a'
down_revision: Union[str, None] = 'cf8e49b6a227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
