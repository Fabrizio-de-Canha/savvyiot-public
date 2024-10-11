"""modify postgres trigger

Revision ID: 4b058458a09a
Revises: af9334703f94
Create Date: 2024-09-21 13:49:37.294753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b058458a09a'
down_revision: Union[str, None] = 'af9334703f94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the PostgreSQL function for notifying tenant-specific updates
    op.execute("""
    CREATE OR REPLACE FUNCTION notify_tenant_update() RETURNS trigger AS $$
    BEGIN
        -- Notify only the relevant tenant by including the tenant_id in the notification channel
        PERFORM pg_notify('tenant_' || NEW.tenant || '_updates', row_to_json(NEW)::text);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Add the trigger to the table for tenant-specific notifications
    op.execute("""
    CREATE TRIGGER tenant_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON devices
    FOR EACH ROW EXECUTE FUNCTION notify_tenant_update();
    """)


def downgrade():
    # Drop the trigger and function in case of rollback
    op.execute("""
    DROP TRIGGER IF EXISTS tenant_update_trigger ON devices;
    """)

    op.execute("""
    DROP FUNCTION IF EXISTS notify_tenant_update;
    """)
