"""Add global_countries table and ics.global_extracted column

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-03-01 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "global_countries",
        sa.Column("iso3", sa.String(3), primary_key=True),
    )
    op.create_index("idx_global_countries_iso3", "global_countries", ["iso3"], unique=True)


def downgrade() -> None:
    op.drop_index("idx_global_countries_iso3", table_name="global_countries")
    op.drop_table("global_countries")
