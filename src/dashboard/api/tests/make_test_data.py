from pathlib import Path
import ast
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
                if csv_name == "WEBSITE_TEXT.csv":
                    row["uk_map_colourramp"] = ast.literal_eval(row["uk_map_colourramp"])
                    row["global_colourramp"] = ast.literal_eval(row["global_colourramp"])
                db_row = model(**row)
                db_session.add(db_row)
    db_session.commit()


def join_tables(dataframes):
    df_topic_weights = dataframes["TOPIC_WEIGHTS_TABLE"][["ics_id", "topic_id", "probability"]]
    df_topics = dataframes["TOPICS_TABLE"][["topic_id", "topic_name"]]
    df_ics = dataframes["ICS_DATABASE_TABLE"][["id", "ukprn", "ics_id", "uoa", "postcode"]]
    df_uoa = dataframes["UOA_TABLE"][["uoa_id", "name", "assessment_group", "assessment_panel"]]
    df_funder = dataframes["ICS_TO_FUNDERS_LOOKUP_TABLE"][["ics_table_id", "funder"]]
    df_countries = dataframes["ICS_TO_COUNTRY_LOOKUP_TABLE"]
    df_inst = dataframes["INSTITUES"][["name", "ukprn"]]
    merged_df = df_topic_weights.merge(df_topics, on='topic_id', how='inner')
    merged_df = merged_df.merge(df_ics, left_on='ics_id', right_on='ics_id', how='inner')
    merged_df = merged_df.merge(df_uoa, left_on='uoa', right_on='uoa_id', how='inner')
    merged_df = merged_df.merge(df_funder, left_on='id', right_on='ics_table_id', how='inner')
    merged_df = merged_df.merge(df_countries, left_on='id', right_on='ics_table_id', how='inner')
    merged_df = merged_df.merge(df_inst, left_on='ukprn', right_on='ukprn', how='inner')
    merged_df.rename(columns={"name_y": "inst_name"}, inplace=True)
    return merged_df


def make_query_table(dataframes,
                     threshold,
                     topic=None,
                     postcode=None,
                     country=None,
                     uoa=None,
                     funder=None,
                     ):
    merged_df = join_tables(dataframes)
    filtered_df = merged_df[merged_df['probability'] >= threshold]
    
    if topic is not None:
        filtered_df = filtered_df[filtered_df['topic_name'] == topic]
    if postcode is not None:
        filtered_df = filtered_df[filtered_df['postcode'] == postcode]
    if country is not None:
        filtered_df = filtered_df[filtered_df['country'] == country]
    if uoa is not None:
        if uoa in ["A", "B", "C", "D"]:
            filtered_df = filtered_df[filtered_df['assessment_panel'] == uoa]
        elif uoa in ["STEM", "SHAPE"]:
            filtered_df = filtered_df[filtered_df['assessment_group'] == uoa]
    if funder is not None:
        filtered_df = filtered_df[filtered_df['funder'] == funder]
    return filtered_df
    
    


