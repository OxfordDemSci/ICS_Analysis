import os
import pandas as pd
import random
import pickle
import re
from dotenv import load_dotenv


# define "basedir" environment variable in ./.env file
load_dotenv()


def iso_to_list(iso_str):
    if isinstance(iso_str, str):
        result = iso_str.split('; ')
    else:
        result = []
    return str(result)


def join_ics(ics, iso):

    # clean ics column names
    ics.columns = ics.columns.str.replace('1. ', '').str.replace('2. ', '').str.replace('3. ', '').\
        str.replace('4. ', '').str.replace('5. ', '')
    ics.columns = ics.columns.str.replace(' ', '_')
    ics.columns = ics.columns.str.lower()
    ics.rename(columns={'ref_impact_case_study_identifier': 'ics_id'}, inplace=True)

    # add clean countries column: Countries -> ISO-3 country codes
    iso.rename(columns={'iso_3_code': 'countries_iso3', 'ref_identifier': 'ics_id'}, inplace=True)

    # join iso3 to ics data
    iso.set_index('ics_id')
    ics.set_index('ics_id')
    result = ics.join(other=iso, rsuffix='_right')
    del result['ics_id_right']

    # reformat iso3 as lists
    result['countries_iso3'] = result['countries_iso3'].apply(iso_to_list)

    return result


if __name__ == '__main__':

    #---- load data ----#

    # define paths
    edit_path = os.path.join(os.getenv('basedir'), 'data', 'edit')
    extra_data_path = os.path.join(os.getenv('basedir'), 'src', 'data_wrangling', '2_enrich_data', 'extra_data')

    enriched_path = os.path.join(os.getenv('basedir'), 'data', 'enriched')
    os.makedirs(enriched_path, exist_ok=True)

    # load ics data
    ics = pd.read_excel(os.path.join(edit_path, 'clean_ref_ics_data.xlsx'))

    # load ics countries as iso-3 codes
    iso = pd.read_csv(os.path.join(extra_data_path, 'iso_3_code.csv'))

    # load institution post codes
    pkl_postcodes = os.path.join(extra_data_path, 'ukprn_postcode_dict.pkl')
    with open(pkl_postcodes, 'rb') as file:
        institution_postcode = pickle.load(file)


    #---- text analysis ----#

    # ## Relevant columns to perform text analysis on
    # text_cols = ['1. Summary of the impact', '2. Underpinning research',
    #              '3. References to the research', '4. Details of the impact',
    #              '5. Sources to corroborate the impact']
    #
    # ## To be replaced by topic models
    # ics['1. Summary of the impact_topic'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    # ics['2. Underpinning research'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    # ics['3. References to the research'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    # ics['4. Details of the impact'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    # ics['5. Sources to corroborate the impact'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    #
    # ## One-hot encode impact type
    # ics = pd.concat([ics, pd.get_dummies(ics['Summary impact type'])], axis=1)


    #---- iso-3 impacted country names ----#

    # add iso3 country codes and clean column names
    ics = join_ics(ics, iso)


    #---- institution postcodes ----#

    # postcodes to ref table
    ics['inst_postcode'] = ics['inst_id'].apply(lambda x: institution_postcode[x])

    # postcode district
    ics['inst_postcode_district'] = ics['inst_postcode'].apply(lambda x: x.split(' ')[0])

    # postcode area
    ics['inst_postcode_area'] = ics['inst_postcode_district'].apply(lambda x: x[0:re.search(r"\d", x).start()])


    #---- url to impact case study summary ----#
    ics['ics_url'] = ics['ics_id'].apply(lambda x: 'https://results2021.ref.ac.uk/impact/' + x + '?page=1')

    #---- Save enriched dataset ----#
    ics.to_csv(os.path.join(enriched_path, 'enriched_ref_ics_data.csv'))
