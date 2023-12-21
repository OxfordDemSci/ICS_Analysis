import ast
import json
import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

from alembic import command
from alembic.config import Config

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR.parent.joinpath(".env")
load_dotenv(ENV_FILE)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
TABLES_DIR = os.environ.get("DATABASE_TABLES_DIR")

try:
    conn = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host="ics_postgres",
        port="5432",
    )
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@ics_postgres:5432/{POSTGRES_DB}"
    )
    pg_host = "ics_postgres"
except psycopg2.OperationalError:
    conn = psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host="localhost",
        port="5432",
    )
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
    )
    pg_host = "localhost"

TABLE_MAP = {
    "ICS_DATABASE_TABLE.csv": {
        "cols_to_convert": ["id", "ukprn"],
        "rename_col": ["covid-statement"],
        "table_name": "ics",
    },
    "ICS_TO_COUNTRY_LOOKUP_TABLE.csv": {
        "cols_to_convert": ["id", "ics_table_id"],
        "table_name": "countries",
    },
    "ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE.csv": {
        "cols_to_convert": ["id", "ics_table_id"],
        "table_name": "uk_regions",
    },
    "ICS_TO_FUNDERS_LOOKUP_TABLE.csv": {
        "cols_to_convert": ["id", "ics_table_id"],
        "table_name": "funder",
    },
    "INSTITUTES.csv": {"cols_to_convert": ["id", "ukprn"], "table_name": "institution"},
    "TOPICS_TABLE.csv": {"cols_to_convert": ["topic_id"], "table_name": "topics"},
    "UOA_TABLE.csv": {"cols_to_convert": ["id", "uoa_id"], "table_name": "uoa"},
    "WEBSITE_TEXT.csv": {"cols_to_convert": ["id"], "table_name": "websitetext"},
    "TOPIC_WEIGHTS_TABLE.csv": {
        "cols_to_convert": ["id", "topic_id"],
        "table_name": "topic_weights",
    },
    "TOPIC_GROUPS_TABLE.csv": {
        "cols_to_convert": ["group_id"],
        "table_name": "topic_groups",
    },
}


def upgrade_alembic():
    alembic_cfg = Config(BASE_DIR.joinpath("alembic.ini"))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{pg_host}:5432/{POSTGRES_DB}",
    )
    command.upgrade(alembic_cfg, "head")


def upload_to_db(df, table_name):
    table_exists = inspect(engine).has_table(table_name)
    if table_exists:
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)
        conn.commit()
        cursor.close()
    if table_name == "websitetext":
        df["uk_map_colourramp"] = df["uk_map_colourramp"].apply(ast.literal_eval)
        df["global_colourramp"] = df["global_colourramp"].apply(ast.literal_eval)
        df["uoa_bar_colours"] = df["uoa_bar_colours"].apply(json.dumps)
    df.to_sql(table_name, engine, if_exists="append", index=False)


def convert_col_to_int(df, col_name):
    df[col_name] = df[col_name].astype(int)
    return df


def rename_col(df, col_name):
    new_col_name = "_".join(col_name.split("-"))
    df = df.rename(columns={col_name: new_col_name})
    return df


def insert_data(table):
    print(f"Uploading {table.name}")
    df = pd.read_csv(table)
    for col in TABLE_MAP[table.name]["cols_to_convert"]:
        df = convert_col_to_int(df, col)
    if "rename_col" in TABLE_MAP[table.name]:
        for col in TABLE_MAP[table.name]["rename_col"]:
            df = rename_col(df, col)
    upload_to_db(df, TABLE_MAP[table.name]["table_name"])
    print(f"{table.name} uploaded to {TABLE_MAP[table.name]['table_name']}")


def upload_tables():
    TABLES = [
        x
        for x in BASE_DIR.joinpath(TABLES_DIR).iterdir()
        if x.name.endswith(".csv")
        if x.name in TABLE_MAP.keys()
    ]
    for table in TABLES:
        insert_data(table)


def alembic_and_insert_tables():
    upgrade_alembic()
    upload_tables()


if __name__ == "__main__":
    alembic_and_insert_tables()
    conn.close()
