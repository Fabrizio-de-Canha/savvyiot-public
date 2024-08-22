"""add surname againnn

Revision ID: 94a85f43acf6
Revises: 7e22df8638a6
Create Date: 2024-08-22 17:55:16.550005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '94a85f43acf6'
down_revision: Union[str, None] = '7e22df8638a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_devices_id', table_name='devices')
    op.drop_index('ix_devices_mac_id', table_name='devices')
    op.drop_table('devices')
    op.drop_table('messages')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('verified', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('active', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('admin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('super_user', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('password', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('last_login', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('password_reset', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('login_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('surname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('tenant_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('message', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('time_received', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.create_table('devices',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('mac_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('active', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('last_reported', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('device_type', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='devices_pkey')
    )
    op.create_index('ix_devices_mac_id', 'devices', ['mac_id'], unique=False)
    op.create_index('ix_devices_id', 'devices', ['id'], unique=False)
    # ### end Alembic commands ###
