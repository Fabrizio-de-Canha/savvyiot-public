"""Add new changes

Revision ID: 21e02f1db02b
Revises: 3064eae55dd4
Create Date: 2024-10-10 14:39:46.743227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21e02f1db02b'
down_revision: Union[str, None] = '3064eae55dd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('verified', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('admin', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_id'), 'test', ['id'], unique=False)
    op.add_column('devices', sa.Column('last_booted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('devices', 'last_booted')
    op.drop_index(op.f('ix_test_id'), table_name='test')
    op.drop_table('test')
    # ### end Alembic commands ###
