"""add surname againn

Revision ID: 7e22df8638a6
Revises: 5aa84cb9cf4a
Create Date: 2024-08-22 17:48:02.323894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7e22df8638a6'
down_revision: Union[str, None] = '5aa84cb9cf4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('mac_id', sa.Text(), nullable=True),
    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('last_reported', sa.DateTime(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('device_type', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_devices_id'), 'devices', ['id'], unique=False)
    op.create_index(op.f('ix_devices_mac_id'), 'devices', ['mac_id'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tenant_id', sa.UUID(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('message', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('time_received', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_index(op.f('ix_devices_mac_id'), table_name='devices')
    op.drop_index(op.f('ix_devices_id'), table_name='devices')
    op.drop_table('devices')
    # ### end Alembic commands ###
