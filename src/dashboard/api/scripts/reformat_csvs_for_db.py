from pathlib import Path
import pandas as pd
from typing import Union
import numpy as np
from dotenv import load_dotenv
import os
import ast


# define "basedir" environment variable in ./.env file
load_dotenv()


BASE_APP = Path(os.getenv('basedir')).joinpath('src', 'dashboard', 'api', 'app', 'data')
BASE = Path(os.getenv('basedir')).resolve()
ENRICHED_ICS_TABLE = BASE.joinpath('data/enriched/enriched_ref_ics_data.csv')
if not ENRICHED_ICS_TABLE.exists():
    raise FileNotFoundError(f'{str(ENRICHED_ICS_TABLE)} is not in place. This file is not held in github and needs to be in {str(ENRICHED_ICS_TABLE.parent)}')
OUTPUT_ICS_TABLE = BASE_APP.joinpath('db-data/ICS_DATABASE_TABLE.csv')


TOPICS_DIR =BASE.joinpath('data/dashboard/nn3nn7')
TOPICS_TABLE = TOPICS_DIR.joinpath('topics.xlsx')
TOPICS_GROUPS_TABLE = TOPICS_DIR.joinpath('topics_groups.xlsx')
WEIGHTS_TABLE = TOPICS_DIR.joinpath('candidate_nn3nn7.xlsx')
TOPICS_OUT = BASE_APP.joinpath('db-data/TOPICS_TABLE.csv')
TOPICS_WEIGHTS_OUT = BASE_APP.joinpath('db-data/TOPIC_WEIGHTS_TABLE.csv')
TOPICS_GROUPS_TABLE = TOPICS_DIR.joinpath('topics_groups.xlsx')
TOPICS_GROUPS_OUT = BASE_APP.joinpath('db-data/TOPIC_GROUPS_TABLE.csv')

FUNDERS_IN = TOPICS_DIR.parent.joinpath('funders.csv')
FUNDERS_LOOKUP_OUT = BASE_APP.joinpath('db-data/ICS_TO_FUNDERS_LOOKUP_TABLE.csv')
COUNTRIES_LOOKUP_OUT = BASE_APP.joinpath('db-data/ICS_TO_COUNTRY_LOOKUP_TABLE.csv')

BASE_CSVS = BASE_APP.joinpath('db-data')
BASE_TEST = BASE_APP.parent.parent.joinpath('tests/test_data')

columns_to_keep = [
    'id',
    'ukprn',
    'institution_name',
    'main_panel',
    'unit_of_assessment_number',
    'unit_of_assessment_name',
    'multiple_submission_letter',
    'multiple_submission_name',
    'joint_submission',
    'ics_id',
    'title',
    'is_continued_from_2014',
    'summary_impact_type',
    'countries',
    'formal_partners',
    'funding_programmes',
    'global_research_identifiers',
    'name_of_funders',
    'researcher_orcids',
    'grant_funding',
    'summary_of_the_impact',
    'underpinning_research',
    'references_to_the_research',
    'details_of_the_impact',
    'sources_to_corroborate_the_impact',
    'covid_statement',
    'uoa',
    'countries_iso3',
    'inst_postcode',
    'inst_postcode_district',
    'postcode',
    'ics_url',
]


def strip_uoa(row):
    uoa_string = row.uoa
    if uoa_string[-1].isalpha():
        uoa_string = uoa_string[:-1]
    
    # Convert the remaining string to an integer
    uoa_int = int(uoa_string)
    
    return uoa_int


def make_ics_table():
    ics_df = pd.read_csv(ENRICHED_ICS_TABLE)
    rename_cols = {'inst_id': 'ukprn', 'uoa_id': 'uoa', 'inst_postcode_area': 'postcode', 'covid-statement': 'covid_statement'}
    ics_df = ics_df.rename(columns=rename_cols)
    ics_df['id'] = ics_df.index.copy().astype(int)
    ics_df['uoa'] = ics_df.apply(strip_uoa, axis=1)
    ics_df = ics_df[columns_to_keep]
    ics_df.to_csv(OUTPUT_ICS_TABLE, index=False)
    return ics_df


def make_funders_lookup_table(df_ics: pd.DataFrame) -> None:
    def transform_funders(row):
        if str(row.funder) != 'nan':
            return [x.lstrip().rstrip() for x in row.funder.split(';')]
        return np.nan
    df_funders = pd.read_csv(FUNDERS_IN)
    df_funders = df_funders[['REF impact case study identifier', 'Funders[full name]']]
    df_funders.rename(columns={"REF impact case study identifier": 'ics_id', 'Funders[full name]': 'funder'}, inplace=True)
    df_ics = df_ics[['id', 'ics_id']]
    df_ics.set_index('ics_id', inplace=True)
    df_funders.set_index('ics_id', inplace=True)
    df_join = df_funders.join(df_ics)
    df_join['funders_list'] = df_join.apply(transform_funders, axis=1)
    df_join.reset_index(inplace=True)
    df_join = df_join[['id', 'funders_list']]
    df_lookup = df_join.explode('funders_list')
    df_lookup.rename(columns={'id': 'ics_table_id', 'funders_list': 'funder'}, inplace=True)
    df_lookup.reset_index(inplace=True)
    df_lookup['id'] = df_lookup.index.copy().astype(int)
    df_lookup = df_lookup.dropna(subset=['ics_table_id'])
    df_lookup["ics_table_id"] = df_lookup["ics_table_id"].astype(int)
    df_lookup = df_lookup[['id', 'ics_table_id', 'funder']]
    df_lookup.to_csv(FUNDERS_LOOKUP_OUT, index=False)


def make_countries_lookup_table(df_ics: pd.DataFrame) -> None:
    df_iso = df_ics[['id', 'countries_iso3']]
    df_iso = df_iso.copy()
    df_iso.loc[:, 'country'] = df_iso.countries_iso3.apply(ast.literal_eval)
    df_iso = df_iso[['id', 'country']]
    df_iso = df_iso.explode('country')
    df_iso = df_iso.rename(columns={'id': 'ics_table_id'})
    df_iso.reset_index(inplace=True)
    df_iso['id'] = df_iso.index.copy().astype(int)
    df_iso = df_iso[['id', 'ics_table_id', 'country']]
    df_iso.to_csv(COUNTRIES_LOOKUP_OUT, index=False)


def make_topics_and_weights(scale_weights: str | None = None) -> None:
    weights_df = pd.read_excel(WEIGHTS_TABLE, sheet_name='Sheet1')
    topics_df = pd.read_excel(TOPICS_TABLE, sheet_name='Sheet1')
    weights_df = weights_df.rename(columns={'REF impact case study identifier': 'ics_id'})
    cols = [x for x in weights_df.columns if isinstance(x, int)]
    cols.insert(0, 'ics_id')

    if scale_weights == 'binary':
        weights_df[cols[1:]] = 0
        for i in range(weights_df.shape[0]):
            weights_df.at[i, weights_df.at[i, 'BERT_topic']] = 1

    weights_df = weights_df[cols]
    weights_df = weights_df.fillna(0)

    if scale_weights == 'maxTo1':
        weights_df[cols[1:]] = weights_df[cols[1:]].apply(lambda x: x.replace(x.max(), 1), axis=1)

    if scale_weights == 'scaleTo1':
        weights_df[cols[1:]] = weights_df[cols[1:]].divide(weights_df[cols[1:]].max(axis=1), axis=0)

    df_long = pd.melt(weights_df, id_vars=['ics_id'], var_name='topic_id', value_name='probability')
    df_long['id'] = df_long.index.copy().astype('int')
    df_long = df_long[['id', 'ics_id', 'topic_id', 'probability']]
    df_long.to_csv(TOPICS_WEIGHTS_OUT, index=False)
    topics_df = topics_df.rename(columns={'Topic Name': 'topic_name_long'})
    topics_df.columns = topics_df.columns.str.lower().str.replace(' ', '_')
    topics_df.to_csv(TOPICS_OUT, index=False)

def make_topics_groups_table():
    group_df = pd.read_excel(TOPICS_GROUPS_TABLE, sheet_name="Sheet1")
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
    df_country.to_csv(BASE_TEST.joinpath("ICS_TO_COUNTRY_LOOKUP_TABLE.csv"), index=False)

    df_funders = pd.read_csv(BASE_CSVS.joinpath("ICS_TO_FUNDERS_LOOKUP_TABLE.csv"))
    df_funders = df_funders[df_funders.ics_table_id.isin(ids)]
    df_funders.to_csv(BASE_TEST.joinpath("ICS_TO_FUNDERS_LOOKUP_TABLE.csv"), index=False)

    df_inst = pd.read_csv(BASE_CSVS.joinpath("INSTITUTES.csv"))
    df_inst = df_inst[df_inst.ukprn.isin(ukprns)]
    df_inst.to_csv(BASE_TEST.joinpath('INSTITUES.csv'), index=False)

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





if __name__ == "__main__":
    print('Making ICS table')
    ics_df = make_ics_table()
    print('Making funders lookup')
    make_funders_lookup_table(ics_df)
    print('Reformatting topics and weights')
    make_topics_and_weights(scale_weights='scaleTo1')
    print("Making topic groups table")
    make_topics_groups_table()
    print("Making countries lookup table")
    make_countries_lookup_table(ics_df)
    print("Making test data")
    making_test_data()