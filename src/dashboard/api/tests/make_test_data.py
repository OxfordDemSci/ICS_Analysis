from pathlib import Path
import csv
from app.models import (
    ICS,
    Topics,
    TopicWeights,
    TopicGroups,
    Funder,
    UOA,
    Institution,
    Countries,
    WebsiteText
)

BASE = Path(__file__).resolve().parent.joinpath('test_data')

csv_map = {
    "ICS_DATABASE_TABLE.csv": ICS,
    "ICS_TO_COUNTRY_LOOKUP_TABLE.csv": Countries,
    "ICS_TO_FUNDERS_LOOKUP_TABLE.csv": Funder,
    "INSTITUES.csv": Institution,
    "TOPIC_GROUPS_TABLE.csv": TopicGroups,
    "TOPIC_WEIGHTS_TABLE.csv": TopicWeights,
    "TOPICS_TABLE.csv": Topics,
    "UOA_TABLE.csv": UOA,
    "WEBSITE_TEXT.csv": WebsiteText
}

def insert_test_data(db_session):
    for csv_name, model in csv_map.items():
        with open(BASE.joinpath(csv_name), 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                db_row = model(**row)
                db_session.add(db_row)
    db_session.commit()
