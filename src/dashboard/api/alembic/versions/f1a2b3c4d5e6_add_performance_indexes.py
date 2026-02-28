"""Add performance indexes

Revision ID: f1a2b3c4d5e6
Revises: 8fbbd4f3ffe8
Create Date: 2026-02-22 17:00:00.000000

"""
from alembic import op

revision = "f1a2b3c4d5e6"
down_revision = "8fbbd4f3ffe8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ics: ics_id is the primary join/filter column across all queries
    op.create_index("idx_ics_ics_id", "ics", ["ics_id"])
    op.create_index("idx_ics_ukprn", "ics", ["ukprn"])

    # topic_weights: starting table for get_ics_sql; all three columns are used
    op.create_index("idx_topic_weights_ics_id", "topic_weights", ["ics_id"])
    op.create_index("idx_topic_weights_topic_id", "topic_weights", ["topic_id"])
    op.create_index("idx_topic_weights_probability", "topic_weights", ["probability"])

    # countries: ics_table_id is the JOIN column, country is the filter
    op.create_index("idx_countries_ics_table_id", "countries", ["ics_table_id"])
    op.create_index("idx_countries_country", "countries", ["country"])

    # funder: ics_table_id is the JOIN column, funder is the filter
    op.create_index("idx_funder_ics_table_id", "funder", ["ics_table_id"])
    op.create_index("idx_funder_funder", "funder", ["funder"])

    # uk_regions: ics_table_id is the JOIN column, tag values is the filter
    op.create_index("idx_uk_regions_ics_table_id", "uk_regions", ["ics_table_id"])
    op.create_index("idx_uk_regions_tag_values", "uk_regions", ["uk_region_tag_values"])

    # institution: ukprn is the JOIN column
    op.create_index("idx_institution_ukprn", "institution", ["ukprn"])

    # uoa: uoa_id is the JOIN column (not the PK id)
    op.create_index("idx_uoa_uoa_id", "uoa", ["uoa_id"])


def downgrade() -> None:
    op.drop_index("idx_uoa_uoa_id", table_name="uoa")
    op.drop_index("idx_institution_ukprn", table_name="institution")
    op.drop_index("idx_uk_regions_tag_values", table_name="uk_regions")
    op.drop_index("idx_uk_regions_ics_table_id", table_name="uk_regions")
    op.drop_index("idx_funder_funder", table_name="funder")
    op.drop_index("idx_funder_ics_table_id", table_name="funder")
    op.drop_index("idx_countries_country", table_name="countries")
    op.drop_index("idx_countries_ics_table_id", table_name="countries")
    op.drop_index("idx_topic_weights_probability", table_name="topic_weights")
    op.drop_index("idx_topic_weights_topic_id", table_name="topic_weights")
    op.drop_index("idx_topic_weights_ics_id", table_name="topic_weights")
    op.drop_index("idx_ics_ukprn", table_name="ics")
    op.drop_index("idx_ics_ics_id", table_name="ics")
