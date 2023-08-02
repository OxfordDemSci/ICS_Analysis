from pathlib import Path
import pandas as pd
from typing import Union

BASE = Path(__file__).resolve().parent.parent.joinpath('app/data')
ENRICHED_ICS_TABLE = BASE.joinpath('intermediate-tables/enriched_ref_ics_data.csv')
if not ENRICHED_ICS_TABLE.exists():
    raise FileNotFoundError(f'{str(ENRICHED_ICS_TABLE)} is not in place. This file is not held in github and needs to be in {str(ENRICHED_ICS_TABLE.parent)}')
OUTPUT_ICS_TABLE = BASE.joinpath('db-data/ICS_DATABASE_TABLE.csv')


TOPICS_DIR = BASE.parent.parent.parent.parent.parent.joinpath('data/dashboard/nn3nn7')
TOPICS_TABLE = TOPICS_DIR.joinpath('topics.xlsx')
WEIGHTS_TABLE = TOPICS_DIR.joinpath('candidate_nn3nn7.xlsx')
TOPICS_OUT = BASE.joinpath('db-data/TOPICS_TABLE.csv')
TOPICS_WEIGHTS_OUT = BASE.joinpath('db-data/TOPIC_WEIGHTS_TABLE.csv')

FUNDERS_LOOKUP_OUT = BASE.joinpath('db-data/ICS_TO_FUNDERS_LOOKUP_TABLE.csv')

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
    transform_funders = lambda x: [funder.strip('[]') for funder in str(x).split(';') if not str(x) == 'nan']
    df_ics['funders_list'] = df_ics['name_of_funders'].apply(transform_funders)
    df_funders_lookup = df_ics[['id', 'funders_list']]
    df_funders_lookup = df_funders_lookup.explode('funders_list')
    df_funders_lookup = df_funders_lookup.rename(columns={'id': 'ics_table_id', 'funders_list': 'funder'})
    df_funders_lookup = df_funders_lookup.dropna()
    df_funders_lookup.to_csv(FUNDERS_LOOKUP_OUT, index=False)

def make_topics_and_weights():
    weights_df = pd.read_excel(WEIGHTS_TABLE, sheet_name='Sheet1')
    topics_df = pd.read_excel(TOPICS_TABLE, sheet_name='Sheet1')
    weights_df = weights_df.rename(columns={'REF impact case study identifier': 'ics_id'})
    cols = [x for x in weights_df.columns if isinstance(x, int)]
    cols.insert(0, 'ics_id')
    weights_df = weights_df[cols]
    weights_df = weights_df.fillna(0)
    df_long = pd.melt(weights_df, id_vars=['ics_id'], var_name='topic_id', value_name='probability')
    df_long['id'] = df_long.index.copy().astype('int')
    df_long = df_long[['id', 'ics_id', 'topic_id', 'probability']]
    df_long.to_csv(TOPICS_WEIGHTS_OUT, index=False)
    topics_df = topics_df.rename(columns={'Topic Name': 'topic_name_long'})
    topics_df.columns = topics_df.columns.str.lower().str.replace(' ', '_')
    topics_df.to_csv(TOPICS_OUT, index=False)

if __name__ == "__main__":
    print('Making ICS table')
    ics_df = make_ics_table()
    print('Making funders lookup')
    make_funders_lookup_table(ics_df)
    print('Reformatting topics and weights')
    make_topics_and_weights()