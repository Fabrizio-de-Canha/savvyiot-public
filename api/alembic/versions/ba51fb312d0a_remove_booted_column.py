"""remove booted column

Revision ID: ba51fb312d0a
Revises: ba6bbd788a6f
Create Date: 2024-10-10 14:13:12.436441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba51fb312d0a'
down_revision: Union[str, None] = 'ba6bbd788a6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
