"""add postgres trigger

Revision ID: 0a4e246a4e59
Revises: ec2d410b8e6e
Create Date: 2024-09-21 11:50:31.741940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a4e246a4e59'
down_revision: Union[str, None] = 'ec2d410b8e6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION notify_table_change() RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify('table_updates', row_to_json(NEW)::text);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER table_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON devices
    FOR EACH ROW EXECUTE FUNCTION notify_table_change();
    """)

def downgrade():
    op.execute("""
    DROP TRIGGER IF EXISTS table_update_trigger ON devices;
    DROP FUNCTION IF EXISTS notify_table_change;
    """)