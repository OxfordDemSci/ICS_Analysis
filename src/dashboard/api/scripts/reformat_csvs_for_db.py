import ast
import os
from pathlib import Path
import shutil

import numpy as np
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv

from csv_to_db_field_name_lookups import COLUMN_CONVERSION_MAP_FROM_CSV, GLOBAL_ISOS, EU_COUNTRIES

# define "basedir" environment variable in ./.env file
load_dotenv()


BASE_APP = Path(os.getenv("basedir")).joinpath("src", "dashboard", "api", "app", "data")
BASE = Path(os.getenv("basedir")).resolve()
ENRICHED_ICS_TABLE = BASE.joinpath("data/final/enhanced_ref_data.zip")
if not ENRICHED_ICS_TABLE.exists():
    raise FileNotFoundError(
        f"{str(ENRICHED_ICS_TABLE)} is not in place. This file is not held in github and needs to be in \
            {str(ENRICHED_ICS_TABLE.parent)}"
    )
OUTPUT_ICS_TABLE = BASE_APP.joinpath("db-data/ICS_DATABASE_TABLE.csv")


TOPICS_DIR = BASE.joinpath("data/dashboard")
TOPICS_TABLE = TOPICS_DIR.joinpath("topics.csv")
TOPIC_NARRATIVES = TOPICS_DIR.joinpath('topic_narrative.csv')
TOPICS_GROUPS_TABLE = TOPICS_DIR.joinpath("topics_groups.csv")
REGIONS_GPKG = TOPICS_DIR.joinpath("UK_REGIONS.gpkg")
TOPICS_OUT = BASE_APP.joinpath("db-data/TOPICS_TABLE.csv")
TOPICS_WEIGHTS_OUT = BASE_APP.joinpath("db-data/TOPIC_WEIGHTS_TABLE.csv")
TOPICS_GROUPS_OUT = BASE_APP.joinpath("db-data/TOPIC_GROUPS_TABLE.csv")

FUNDERS_IN = TOPICS_DIR.joinpath("funders.csv")
FUNDERS_LOOKUP_OUT = BASE_APP.joinpath("db-data/ICS_TO_FUNDERS_LOOKUP_TABLE.csv")
COUNTRIES_LOOKUP_OUT = BASE_APP.joinpath("db-data/ICS_TO_COUNTRY_LOOKUP_TABLE.csv")
UK_REGIONS_LOOKUP_OUT = BASE_APP.joinpath("db-data/ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE.csv")
UK_REGIONS_GEOM_TABLE = BASE_APP.joinpath("db-data/REGIONS_GEOMETRY_TABLE.csv")

BASE_CSVS = BASE_APP.joinpath("db-data")
BASE_TEST = BASE_APP.parent.parent.joinpath("tests/test_data")


def strip_uoa(row):
    if isinstance(row.uoa, str):
        uoa_string = row.uoa
        if uoa_string[-1].isalpha():
            uoa_string = uoa_string[:-1]

    # Convert the remaining string to an integer
        uoa_int = int(uoa_string)
    else:
        uoa_int = int(row.uoa)

    return uoa_int


def make_ics_table():
    ics_df = pd.read_csv(ENRICHED_ICS_TABLE)
    ics_df = ics_df.rename(columns=COLUMN_CONVERSION_MAP_FROM_CSV)
    ics_df["id"] = ics_df.index.copy().astype(int)
    ics_df["uoa"] = ics_df.apply(strip_uoa, axis=1)
    ics_df.to_csv(OUTPUT_ICS_TABLE, index=False)
    return ics_df


def make_funders_lookup_table(df_ics: pd.DataFrame) -> None:
    def transform_funders(row):
        if str(row.funder) != "nan":
            return [x.lstrip().rstrip() for x in row.funder.split(";")]
        return np.nan

    df_funders = pd.read_csv(FUNDERS_IN)
    df_funders = df_funders[["REF impact case study identifier", "Funders[full name]"]]
    df_funders.rename(
        columns={
            "REF impact case study identifier": "ics_id",
            "Funders[full name]": "funder",
        },
        inplace=True,
    )
    df_ics = df_ics[["id", "ics_id"]]
    df_ics.set_index("ics_id", inplace=True)
    df_funders.set_index("ics_id", inplace=True)
    df_join = df_funders.join(df_ics)
    df_join["funders_list"] = df_join.apply(transform_funders, axis=1)
    df_join.reset_index(inplace=True)
    df_join = df_join[["id", "funders_list"]]
    df_lookup = df_join.explode("funders_list")
    df_lookup.rename(
        columns={"id": "ics_table_id", "funders_list": "funder"}, inplace=True
    )
    df_lookup.reset_index(inplace=True)
    df_lookup["id"] = df_lookup.index.copy().astype(int)
    df_lookup = df_lookup.dropna(subset=["ics_table_id"])
    df_lookup["ics_table_id"] = df_lookup["ics_table_id"].astype(int)
    df_lookup = df_lookup[["id", "ics_table_id", "funder"]]
    df_lookup.to_csv(FUNDERS_LOOKUP_OUT, index=False)


def fix_errors(row):
    if pd.notna(row.countries_iso3):
        if "global" in row.countries_iso3:
            return ", ".join(GLOBAL_ISOS)
        elif ("europe" in row.countries_iso3) and ("global" not in row.countries_iso3):
            return ", ".join(EU_COUNTRIES)
        elif "VUTl" in row.countries_iso3:
            row.countries_iso3 = row.countries_iso3.replace("VUTl", "VUT")
            return row.countries_iso3
        elif "USA SWE" in row.countries_iso3:
            row.countries_iso3 = row.countries_iso3.replace("USA SWE", "USA, SWE")
            return row.countries_iso3
        else:
            return row.countries_iso3
    else:
        return row.countries_iso3


def make_countries_lookup_table(df_ics: pd.DataFrame) -> None:
    df_iso = df_ics[["id", "countries_iso3"]]
    df_iso = df_iso.copy()
    df_iso["countries_iso3"] = df_iso["countries_iso3"].str.replace(";", ",").str.replace(":", ",")
    df_iso["countries_iso3"] = df_iso.apply(fix_errors, axis=1)
    df_iso.loc[:, "country"] = df_iso.countries_iso3.str.split(",")
    df_iso = df_iso[["id", "country"]]
    df_iso = df_iso.explode("country")
    df_iso = df_iso.rename(columns={"id": "ics_table_id"})
    df_iso.reset_index(inplace=True)
    df_iso["id"] = df_iso.index.copy().astype(int)
    df_iso = df_iso[["id", "ics_table_id", "country"]]
    df_iso.country = df_iso.country.str.strip()
    df_iso.country = df_iso.country.replace('', np.nan)
    df_iso.to_csv(COUNTRIES_LOOKUP_OUT, index=False)


def make_uk_region_tag_lookup_table(df_ics: pd.DataFrame) -> list:
    df_iso = df_ics[["id", "uk_region_tag_values"]]
    df_iso = df_iso.copy()
    df_iso.loc[:, "uk_region_tag_values"] = df_iso.uk_region_tag_values.apply(ast.literal_eval)
    df_iso = df_iso[["id", "uk_region_tag_values"]]
    df_iso = df_iso.explode("uk_region_tag_values")
    df_iso = df_iso.rename(columns={"id": "ics_table_id"})
    df_iso.reset_index(inplace=True)
    df_iso["uk_region_tag_values"] = df_iso["uk_region_tag_values"].apply(
        lambda x: x.lower().title() if pd.notnull(x) else x
    )
    df_iso["id"] = df_iso.index.copy().astype(int)
    df_iso = df_iso[["id", "ics_table_id", "uk_region_tag_values"]]
    df_iso.to_csv(UK_REGIONS_LOOKUP_OUT, index=False)
    return [x for x in df_iso.uk_region_tag_values.unique().tolist() if pd.notnull(x)]


def make_uk_region_geom_table(region_list) -> None:
    gdf = gpd.read_file(REGIONS_GPKG)
    gdf["regions_wkt"] = gdf.apply(lambda x: x.geometry.wkt, axis=1)
    df = pd.DataFrame(gdf[[x for x in gdf.columns if x not in ["geometry", "country", "index"]]])  # Geom not saved as binary in DB
    df["PLACENAME"] = df["PLACENAME"].apply(lambda x: x.lower().title() if pd.notnull(x) else x)
    try:
        assert sorted(df.PLACENAME.unique().tolist()) == sorted(region_list)
    except AssertionError:
        raise ValueError(
            f"{UK_REGIONS_GEOM_TABLE.name} not saved because regions in this table differ from uk_region_tag_values in {UK_REGIONS_LOOKUP_OUT.name}."
            f"Please fix this mismatch before running this script again"
            )
    df.to_csv(UK_REGIONS_GEOM_TABLE, index=False)


def make_weights_df_binary_per_ics(topic_ids: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    ics_id = row.ics_id
    topic_id = row.topic_id
    df_ = pd.DataFrame(data={'ics_id': [ics_id], 'topic_id': [topic_id], 'probability': [1]}).set_index('topic_id')
    df_subset = topic_ids.join(df_, how='outer')
    df_subset.ics_id = df_subset.ics_id.fillna(ics_id)
    df_subset.probability = df_subset.probability.fillna(0)
    return df_subset


def make_topics_and_weights(ics_df: pd.DataFrame, scale_weights: str | None = None) -> None:
    topics_df = pd.read_csv(TOPICS_TABLE)
    topic_narratives_df = pd.read_csv(TOPIC_NARRATIVES).set_index('topic_id')
    topic_ids = topics_df[['topic_id']].copy().set_index('topic_id')
    # TODO
    cols = None  # To be implemented later
    # weights_df = weights_df.rename(
    #     columns={"REF impact case study identifier": "ics_id"}
    # # )

    # cols = [x for x in weights_df.columns if isinstance(x, int)]
    # cols.insert(0, "ics_id")

    if scale_weights == "binary":
        # weights_df[cols[1:]] = 0
        # for i in range(weights_df.shape[0]):
        #     weights_df.at[i, weights_df.at[i, "BERT_topic"]] = 1
        topic_weights_dfs_to_join = []
        for _, row in ics_df.iterrows():
            if pd.notna(row.topic_id):
                df_subset = make_weights_df_binary_per_ics(topic_ids, row)
                topic_weights_dfs_to_join.append(df_subset.reset_index())
        df_topic_weights_final = pd.concat(topic_weights_dfs_to_join).reset_index()
        df_topic_weights_final["id"] = df_topic_weights_final.index.copy().astype("int")
        cols = [x for x in df_topic_weights_final.columns if x not in ['id', 'index']]
        cols.insert(0, 'id')
        df_topic_weights_final = df_topic_weights_final[cols]
        df_topic_weights_final.to_csv(TOPICS_WEIGHTS_OUT, index=False)

    else:
        raise NotImplementedError("Only 'binary' option is currently implemented")

    # FIXME this will need to be decided/implemented later - Only binary option now
    # weights_df = weights_df[cols]
    # weights_df = weights_df.fillna(0)

    # if scale_weights == "maxTo1":
    #     weights_df[cols[1:]] = weights_df[cols[1:]].apply(
    #         lambda x: x.replace(x.max(), 1), axis=1
    #     )

    # if scale_weights == "scaleTo1":
    #     weights_df[cols[1:]] = weights_df[cols[1:]].divide(
    #         weights_df[cols[1:]].max(axis=1), axis=0
    #     )

    # df_long = pd.melt(
    #     weights_df, id_vars=["ics_id"], var_name="topic_id", value_name="probability"
    # )
    # df_long["id"] = df_long.index.copy().astype("int")
    # df_long = df_long[["id", "ics_id", "topic_id", "probability"]]
    # df_long.to_csv(TOPICS_WEIGHTS_OUT, index=False)
    # topics_df = topics_df.rename(columns={"Topic Name": "topic_name_long"})
    # topics_df.columns = topics_df.columns.str.lower().str.replace(" ", "_")
    topics_df = topics_df[
        [
            "topic_id",
            "group_id",
            "topic_group",
            "topic_name",
            "topic_name_long",
            "description",
            "narrative",
            "keywords",
        ]
    ]
    def make_narrative_html(row):
        narratives = topic_narratives_df.loc[row.topic_id]
        nar_str = ''
        if isinstance(narratives, pd.DataFrame):
            for row in narratives.itertuples():
                nar_str += f'<h6>{row.name}</h6>\n<p>{row.description}\n<a href="{row.url}" target="_blank">Read more...</a></p>\n'
        else:
            nar_str += f'<h6>{narratives["name"]}</h6>\n<p>{narratives.description}\n<a href="{narratives.url}" target="_blank">Read more...</a></p>\n'
        return nar_str
    topics_df['narrative'] = topics_df.apply(make_narrative_html, axis=1)
    topics_df.to_csv(TOPICS_OUT, index=False)


def make_topics_groups_table():
    group_df = pd.read_csv(TOPICS_GROUPS_TABLE)
    if np.all(group_df.narrative == "none"):
        group_df["narrative"] = np.nan
    group_df.to_csv(TOPICS_GROUPS_OUT, index=False)


def making_test_data():
    ics = pd.read_csv(BASE_CSVS.joinpath("ICS_DATABASE_TABLE.csv"))
    ics = ics.sample(frac=1).reset_index(drop=True)
    ics_ids = ics.ics_id.tolist()[0:99]
    ids = ics.id.tolist()[0:99]
    ukprns = ics.ukprn.tolist()[0:99]
    ics = ics[ics.ics_id.isin(ics_ids)]
    ics.to_csv(BASE_TEST.joinpath("ICS_DATABASE_TABLE.csv"), index=False)

    df_country = pd.read_csv(BASE_CSVS.joinpath("ICS_TO_COUNTRY_LOOKUP_TABLE.csv"))
    df_country = df_country[df_country.ics_table_id.isin(ids)]
    df_country.to_csv(
        BASE_TEST.joinpath("ICS_TO_COUNTRY_LOOKUP_TABLE.csv"), index=False
    )

    df_regions_lookup = pd.read_csv(BASE_CSVS.joinpath("ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE.csv"))
    df_regions_lookup = df_regions_lookup[df_regions_lookup.ics_table_id.isin(ids)]
    df_regions_lookup.to_csv(
        BASE_TEST.joinpath("ICS_TO_UK_REGIONS_TAG_LOOKUP_TABLE.csv")
    )

    df_funders = pd.read_csv(BASE_CSVS.joinpath("ICS_TO_FUNDERS_LOOKUP_TABLE.csv"))
    df_funders = df_funders[df_funders.ics_table_id.isin(ids)]
    df_funders.to_csv(
        BASE_TEST.joinpath("ICS_TO_FUNDERS_LOOKUP_TABLE.csv"), index=False
    )

    df_inst = pd.read_csv(BASE_CSVS.joinpath("INSTITUTES.csv"))
    df_inst = df_inst[df_inst.ukprn.isin(ukprns)]
    df_inst.to_csv(BASE_TEST.joinpath("INSTITUTES.csv"), index=False)

    df_topic_groups = pd.read_csv(BASE_CSVS.joinpath("TOPIC_GROUPS_TABLE.csv"))
    df_topic_groups.to_csv(BASE_TEST.joinpath("TOPIC_GROUPS_TABLE.csv"), index=False)

    df_weights = pd.read_csv(BASE_CSVS.joinpath("TOPIC_WEIGHTS_TABLE.csv"))
    df_weights = df_weights[df_weights.ics_id.isin(ics_ids)]
    df_weights.to_csv(BASE_TEST.joinpath("TOPIC_WEIGHTS_TABLE.csv"), index=False)

    df_topics = pd.read_csv(BASE_CSVS.joinpath("TOPICS_TABLE.csv"))
    df_topics.to_csv(BASE_TEST.joinpath("TOPICS_TABLE.csv"), index=False)

    df_uoa = pd.read_csv(BASE_CSVS.joinpath("UOA_TABLE.csv"))
    df_uoa.to_csv(BASE_TEST.joinpath("UOA_TABLE.csv"), index=False)

    df_websitetext = pd.read_csv(BASE_CSVS.joinpath("WEBSITE_TEXT.csv"))
    df_websitetext.to_csv(BASE_TEST.joinpath("WEBSITE_TEXT.csv"), index=False)

    df_regions = pd.read_csv(BASE_CSVS.joinpath("REGIONS_GEOMETRY_TABLE.csv"))
    df_regions.to_csv(BASE_TEST.joinpath("REGIONS_GEOMETRY_TABLE.csv"), index=False)


if __name__ == "__main__":
    print("Making ICS table")
    ics_df = make_ics_table()
    print("Making funders lookup")
    make_funders_lookup_table(ics_df)
    print("Reformatting topics and weights")
    make_topics_and_weights(ics_df, scale_weights="binary")
    print("Making topic groups table")
    make_topics_groups_table()
    print("Making countries lookup table")
    make_countries_lookup_table(ics_df)
    print("Making UK regions lookup table")
    region_list = make_uk_region_tag_lookup_table(ics_df)
    make_uk_region_geom_table(region_list)
    for table in ["WEBSITE_TEXT.csv", "INSTITUTES.csv", "UOA_TABLE.csv"]:
        dst = BASE_CSVS.joinpath(table)
        src = TOPICS_DIR.joinpath('backup_tables_DO_NOT_DELETE', table)
        if not dst.exists():
            print('copying hardcoded tables')
            shutil.copy(src, dst)
    print("Making test data")
    making_test_data()
