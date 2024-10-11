"""add booted column

Revision ID: ba6bbd788a6f
Revises: 242c81639a7a
Create Date: 2024-10-10 14:03:27.280290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba6bbd788a6f'
down_revision: Union[str, None] = '242c81639a7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
