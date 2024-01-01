import ast
import csv
import json
import pandas as pd
from pathlib import Path

from app.models import (ICS, UOA, Countries, Funder, Institution, TopicGroups,
                        Topics, TopicWeights, UKRegions, RegionsGeometry, WebsiteText)

BASE = Path(__file__).resolve().parent.joinpath("test_data")

csv_map = {
    "ICS_DATABASE_TABLE.csv": ICS,
    "ICS_TO_COUNTRY_LOOKUP_TABLE.csv": Countries,
    "ICS_TO_FUNDERS_LOOKUP_TABLE.csv": Funder,
    "INSTITUTES.csv": Institution,
    "TOPIC_GROUPS_TABLE.csv": TopicGroups,
    "TOPIC_WEIGHTS_TABLE.csv": TopicWeights,
    "TOPICS_TABLE.csv": Topics,
    "UOA_TABLE.csv": UOA,
    "WEBSITE_TEXT.csv": WebsiteText,
    "ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE.csv": UKRegions,
    "REGIONS_GEOMETRY_TABLE.csv": RegionsGeometry,
}


def insert_test_data(db_session):
    for csv_name, model in csv_map.items():
        df = pd.read_csv(BASE.joinpath(csv_name))
        if csv_name == "WEBSITE_TEXT.csv":
            df["uk_map_colourramp"] = df["uk_map_colourramp"].apply(ast.literal_eval)
            df["global_colourramp"] = df["global_colourramp"].apply(ast.literal_eval)
            df["uoa_bar_colours"] = df["uoa_bar_colours"].apply(json.dumps)
        data = df.to_dict(orient="records")
        for row in data:
            db_row = model(**row)
            db_session.add(db_row)
    db_session.commit()


def join_tables(dataframes):
    df_topic_weights = dataframes["TOPIC_WEIGHTS_TABLE"][
        ["ics_id", "topic_id", "probability"]
    ]
    df_topics = dataframes["TOPICS_TABLE"][["topic_id", "topic_name"]]
    df_ics = dataframes["ICS_DATABASE_TABLE"][
        ["id", "ukprn", "ics_id", "uoa", "postcode"]
    ]
    df_ics["uoa"] = df_ics.uoa.astype(int)
    df_uoa = dataframes["UOA_TABLE"][
        ["uoa_id", "name", "assessment_group", "assessment_panel"]
    ]
    df_funder = dataframes["ICS_TO_FUNDERS_LOOKUP_TABLE"][["ics_table_id", "funder"]]
    df_countries = dataframes["ICS_TO_COUNTRY_LOOKUP_TABLE"]
    df_regions = dataframes["ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE"]
    df_inst = dataframes["INSTITUTES"][["name", "ukprn"]]
    merged_df = df_topic_weights.merge(df_topics, on="topic_id", how="inner")
    merged_df = merged_df.merge(
        df_ics, left_on="ics_id", right_on="ics_id", how="inner"
    )
    merged_df = merged_df.merge(df_uoa, left_on="uoa", right_on="uoa_id", how="inner")
    merged_df = merged_df.merge(
        df_funder, left_on="id", right_on="ics_table_id", how="inner"
    )
    merged_df = merged_df.merge(
        df_countries, left_on="id", right_on="ics_table_id", how="inner"
    )
    merged_df = merged_df.merge(
        df_regions, left_on="id_x", right_on="ics_table_id", how="inner"
    )
    merged_df = merged_df.merge(df_inst, left_on="ukprn", right_on="ukprn", how="inner")
    merged_df.rename(columns={"name_y": "inst_name"}, inplace=True)
    return merged_df


def make_query_table(
    dataframes,
    threshold,
    topic=None,
    postcode=None,
    country=None,
    uk_region=None,
    uoa=None,
    funder=None,
):
    merged_df = join_tables(dataframes)
    filtered_df = merged_df[merged_df["probability"] >= threshold]
    if topic is not None:
        filtered_df = filtered_df[filtered_df["topic_name"] == topic]
    if postcode is not None:
        filtered_df = filtered_df[filtered_df["postcode"] == postcode]
    if country is not None:
        filtered_df = filtered_df[filtered_df["country"] == country]
    if uk_region is not None:
        filtered_df = filtered_df[filtered_df["uk_region_tag_values"] == uk_region]
    if uoa is not None:
        if uoa in ["A", "B", "C", "D"]:
            filtered_df = filtered_df[filtered_df["assessment_panel"] == uoa]
        elif uoa in ["STEM", "SHAPE"]:
            filtered_df = filtered_df[filtered_df["assessment_group"] == uoa]
    if funder is not None:
        filtered_df = filtered_df[filtered_df["funder"] == funder]
    return filtered_df
