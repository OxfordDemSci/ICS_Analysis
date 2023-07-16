from os.path import join
from os import listdir
import requests
import os
import pandas as pd
import numpy as np
#from dotenv import load_dotenv
from pathlib import Path
#load_dotenv()  # define "basedir" environment variable in ./.env file
import random
import pickle
import re


def get_impact_data(raw_path):
    """Grab raw REF Impact Data"""
    """ A function to get the raw ICS data"""
    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_ics_data.xlsx'), 'wb').write(r.content)


def get_environmental_data(raw_path):
    """Grab raw REF Environment Data"""
    """ A function to get the raw environmental data"""
    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_environment_data.xlsx'), 'wb').write(r.content)


def get_all_results(raw_path):
    """Grab raw REF Results Data"""
    """ A function to get the raw results data"""
    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_results_data.xlsx'), 'wb').write(r.content)


def get_output_data(raw_path):
    """Grab raw REF OutPut Data"""
    """ A function to get the raw output data"""
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_outputs_data.xlsx'), 'wb').write(r.content)

def check_id_overlap(a, b):
    ###Convenience function to check overlap of two lists of ids"""
    
    print("{} of element in B present in A".format(
        np.mean([i in a for i in b])))
    print("{} of element in A present in B".format(
        np.mean([i in b for i in a])))

    print("{} missing in A but present in B".format(
        [i for i in a if i not in b]))
    print("{} missing in B but present in A".format(
        [i for i in b if i not in a]))

def format_ids(df):
    """Format id codes for merging"""
    if 'Institution UKPRN code' in df.columns:
        df = df.rename(
            columns={'Institution UKPRN code': 'inst_id'})
    if 'Institution code (UKPRN)' in df.columns:
        df = df.rename(
            columns={'Institution code (UKPRN)': 'inst_id'})
    
    print("{} row(s) dropped due to NA inst_id".\
        format((df['inst_id'] == ' ').sum()))
        
    df = df.copy()[df['inst_id'] != ' ']
    df = df.astype({'inst_id': 'int'})
    df['uoa_id'] = df['Unit of assessment number'].astype(int).astype(
        str) + df['Multiple submission letter'].fillna('').astype(str)
    return(df)

def merge_ins_uoa(df1, df2):
    """Function to merge df2 left on df1 based on inst_id and uoa_id"""

    ## [TODO] Add further unit tests on the merge here ##
    assert all(df1['inst_id'].isin(df2['inst_id']))
    assert all(df1['uoa_id'].isin(df2['uoa_id']))
    
    return(df1.merge(df2, how='left', left_on=['inst_id', 'uoa_id'],
                     right_on=['inst_id', 'uoa_id']))


def clean_ics_level(raw_path, edit_path):
    ## Add stars to ICS level
    raw_ics = pd.read_excel(
        os.path.join(raw_path,
                     'raw_ref_ics_data.xlsx'))
    [n_ics, k_ics] = raw_ics.shape
    raw_ics = format_ids(raw_ics)
    raw_ics.to_excel(os.path.join(edit_path, 'clean_ref_ics_data.xlsx'))

def clean_dep_level(raw_path, edit_path):
    
    ## Generate wide score card at department level
    raw_results = pd.read_excel(os.path.join(raw_path,
                                             'raw_ref_results_data.xlsx'),
                                skiprows=6)
    [n_results, k_results] = raw_results.shape
    raw_results = format_ids(raw_results)
    raw_results = raw_results.rename(
        columns={'FTE of submitted staff': 'fte',
                 '% of eligible staff submitted': 'fte_pc'})
    
    ## Make wide score card by institution and uoa_id
    score_types = ['4*', '3*', '2*', '1*', 'Unclassified'] # types of scores
    wide_score_card = pd.pivot(
        raw_results[['inst_id', 'uoa_id', 'Profile'] + score_types],
        index=['inst_id', 'uoa_id'], columns=['Profile'], values=score_types)
    wide_score_card.columns = wide_score_card.columns.map('_'.join)
    wide_score_card = wide_score_card.reset_index()
    
    ## Obtain relevant environment data
    raw_env_path = os.path.join(raw_path, 'raw_ref_environment_data.xlsx')
    raw_env_doctoral = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchDoctoralDegreesAwarded", skiprows=4)
    raw_env_doctoral = format_ids(raw_env_doctoral)
    number_cols = [col for col in raw_env_doctoral.columns if 'Number of doctoral' in col]
    raw_env_doctoral['num_doc_degrees_total'] = raw_env_doctoral[number_cols].sum(axis=1)

    # 3.2. Sheet Two: Research income
    raw_env_income = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchIncome", skiprows=4)
    raw_env_income = format_ids(raw_env_income)
    raw_env_income = raw_env_income.\
        rename(columns = {'Average income for academic years 2013-14 to 2019-20': 'av_income',
                          'Total income for academic years 2013-14 to 2019-20': 'tot_income'})
    tot_inc = raw_env_income[raw_env_income['Income source'] == 'Total income']

    # 3.3. Research Income In-Kind
    raw_env_income_inkind = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchIncomeInKind", skiprows=4)
    raw_env_income_inkind = format_ids(raw_env_income_inkind)
    raw_env_income_inkind = raw_env_income_inkind.rename(
        columns={'Total income for academic years 2013-14 to 2019-20': 'tot_inc_kind'})

    tot_inc_kind = raw_env_income_inkind.loc[raw_env_income_inkind['Income source']=='Total income-in-kind']    

    ## Merge all dept level data together
    raw_dep = merge_ins_uoa(raw_results[['inst_id', 'uoa_id', 'fte', 'fte_pc']].drop_duplicates(),
                             wide_score_card)
    raw_dep = merge_ins_uoa(raw_dep,
                             raw_env_doctoral[['inst_id', 'uoa_id', 'num_doc_degrees_total']])
    raw_dep = merge_ins_uoa(raw_dep,
                             tot_inc[['inst_id', 'uoa_id', 'av_income', 'tot_income']])
    raw_dep = merge_ins_uoa(raw_dep,
                             tot_inc_kind[['inst_id', 'uoa_id', 'tot_inc_kind']])
    raw_dep.to_excel(os.path.join(edit_path, 'clean_ref_dep_data.xlsx'))
    
    
def clean_output_level(raw_path, edit_path):
    raw_output = pd.read_excel(os.path.join(raw_path, 'raw_ref_outputs_data.xlsx'), skiprows=4)
    raw_output = format_ids(raw_output)
    raw_output.to_excel(os.path.join(edit_path, 'clean_ref_output_data.xlsx'))


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



def main(basedir, outdir):
    raw_path = basedir.joinpath('data', 'raw')
    data_files = [f for f in raw_path.iterdir()]
    
    if ~('raw_ref_environment_data.xlsx' in data_files):
        get_environmental_data(raw_path)
    if ~('raw_ref_ics_data.xlsx' in data_files):
        get_impact_data(raw_path)
    if ~('raw_ref_results_data.xlsx' in data_files):
        get_all_results(raw_path)
    if ~('raw_ref_outputs_data.xlsx' in data_files):
        get_output_data(raw_path)
    print('PART 1 Done...')

    edit_path = basedir.joinpath('data', 'edit')
    #raw_path = os.path.join(os.getenv('basedir'), 'data', 'raw')
    #edit_path = os.path.join(os.getenv('basedir'), 'data', 'edit')
    os.makedirs(edit_path, exist_ok=True)
    clean_ics_level(raw_path, edit_path)
    clean_dep_level(raw_path, edit_path)
    clean_output_level(raw_path, edit_path)
    print("PART 2 Done...")

    #---- load data ----#

    # define paths
    edit_path = basedir.joinpath('data', 'edit')
    extra_data_path = basedir.joinpath('src', 'data_wrangling', '2_enrich_data', 'extra_data')


    enriched_path = outdir.joinpath('enriched')
    os.makedirs(enriched_path, exist_ok=True)

    # load ics data
    ics = pd.read_excel(edit_path.joinpath('clean_ref_ics_data.xlsx'))

    # load ics countries as iso-3 codes
    iso = pd.read_csv(extra_data_path.joinpath('iso_3_code.csv'))

    # load institution post codes
    pkl_postcodes = extra_data_path.joinpath('ukprn_postcode_dict.pkl')
    with open(pkl_postcodes, 'rb') as file:
        institution_postcode = pickle.load(file)


    #---- text analysis ----#

    ## Relevant columns to perform text analysis on
    text_cols = ['1. Summary of the impact', '2. Underpinning research',
                 '3. References to the research', '4. Details of the impact',
                 '5. Sources to corroborate the impact']

    ## To be replaced by topic models
    ics['1. Summary of the impact_topic'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    ics['2. Underpinning research'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    ics['3. References to the research'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    ics['4. Details of the impact'] = [random.randint(1, 10) for i in range(ics.shape[0])]
    ics['5. Sources to corroborate the impact'] = [random.randint(1, 10) for i in range(ics.shape[0])]

    ## One-hot encode impact type
    ics = pd.concat([ics, pd.get_dummies(ics['Summary impact type'])], axis=1)


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


    #---- Save enriched dataset ----#
    ics.to_csv(enriched_path.joinpath('enriched_ref_ics_data.csv'), index=False)
    print("Part 3 Done... Enriched data made. Now making ICS_DATABASE_Table")
    
    ics['id'] = ics.index
    ics = ics[['id', 'inst_id',  'institution_name','inst_postcode_area', 'ics_id', 'countries_iso3', 'name_of_funders', 'uoa_id']]
    ics.rename(columns={
                    'inst_id': 'ukprn',
                    'inst_postcode_area': 'postcode',
                    'countries_iso3': 'countries',
                    'name_of_funders': 'funders',
                    'uoa_id': 'uoa',
                    }, inplace=True)
    ics.to_csv(enriched_path.parent.joinpath('ICS_DATABASE_TABLE.csv'), index=False)





if __name__ == "__main__":
    basedir = Path(__file__).resolve().parent.parent.parent.parent
    outdir = Path(__file__).resolve().parent.joinpath('data')
    main(basedir, outdir)