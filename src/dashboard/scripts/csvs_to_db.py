"""NOTE: This script will upload ALL csvs in /data/for_db to the ics database, create a dump for the database and save this into the sql docker environment of the application."""
from pathlib import Path
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

env_file = Path(__file__).resolve().parent.joinpath('postgres_local_dev/.env')
load_dotenv(env_file)
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

BASE = Path('.').resolve().joinpath('data/for_db')

conn = psycopg2.connect(database='ics', user=db_user, password=db_password, host='localhost', port='5432')
engine = create_engine('postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/ics')


table_col_to_conversion_func_map = {
    "ICS_DATABASE_TABLE": {
        "int": ["id", "ukprn"],
        "list": None,
        "table": "ics"
    },
    "ICS_TO_COUNTRY_LOOKUP_TABLE": {
        "int": ["id", "ics_table_id"],
        "list": None,
        "table": "countries",

    },
    "ICS_TO_FUNDERS_LOOKUP_TABLE": {
        "int": ["id", "ics_table_id"],
        "list": None,
        "table": "funder"
    },
    "INSTITUTES": {
        "int": ["id", "ukprn"],
        "list": None,
        "table": "institution",
    },
    "TOPICS_TABLE": {
        "int": ["id", "topic_id"],
        "list": None,
        "table": "topics",
    },
    "TOPIC_WEIGHTS_TABLE": {
        "int": ["id", "topic_id"],
        "list": None,
        "table": "topic_weights",
    },
    "UOA_TABLE": {
        "int": ["id", "uoa_id"],
        "list": None,
        "table": "uoa",
    },
    "WEBSITE_TEXT": {
        "int": ["id"],
        "list": None,
        "table": "websitetext",
    },

}


def main():
    CSVS = [x for x in BASE.iterdir() if x.name.endswith('.csv')]
    for csv in CSVS:
        print(csv.name)


def upload_to_db(df, table_name):
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
def convert_col_to_int(df, col_name):
    df[col_name] = df[col_name].astype(int)
    return df

def convert_col_to_list(df, col_name):
    pass


if __name__ == "__main__":
    main()