from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent.joinpath('app/data')
ENRICHED_ICS_TABLE = BASE.joinpath('intermediate-tables/enriched_ref_ics_data.csv')
if not ENRICHED_ICS_TABLE.exists():
    raise FileNotFoundError(f'{str(ENRICHED_ICS_TABLE)} is not in place. This file is not held in github and needs to be in {str(ENRICHED_ICS_TABLE.parent)}')
OUTPUT_ICS_TABLE = BASE.joinpath('db-data/ICS_DATABASE_TABLE.csv')

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

def make_ics_table():
    ics_df = pd.read_csv(ENRICHED_ICS_TABLE)
    rename_cols = {'inst_id': 'ukprn', 'uoa_id': 'uoa', 'inst_postcode_area': 'postcode', 'covid-statement': 'covid_statement'}
    ics_df = ics_df.rename(columns=rename_cols)
    ics_df['id'] = ics_df.index.copy().astype(int)
    ics_df = ics_df[columns_to_keep]
    ics_df.to_csv(OUTPUT_ICS_TABLE, index=False)


if __name__ == "__main__":
    make_ics_table()