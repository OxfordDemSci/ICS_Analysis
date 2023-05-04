from os.path import isfile, join
from os import listdir
import requests
import os
import pandas as pd
import numpy as np


def get_impact_data(raw_path):
    """Grab raw REF Impact Data"""
    """ A function to get the raw ICS data"""
    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ics_data.xlsx'), 'wb').write(r.content)


def get_environmental_data(raw_path):
    """Grab raw REF Environment Data"""
    """ A function to get the raw environmental data"""
    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_environment_data.xlsx'), 'wb').write(r.content)


def get_output_data(raw_path):
    """Grab raw REF OutPut Data"""
    """ A function to get the raw output data"""
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_outputs_data.xlsx'), 'wb').write(r.content)


def get_all_results(raw_path):
    """Grab raw REF Results Data"""
    """ A function to get the raw results data"""
    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_results_data.xlsx'), 'wb').write(r.content)

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

    df = df.astype({'inst_id': 'int'})
    df['uoa_id'] = df['Unit of assessment number'].astype(int).astype(
        str) + df['Multiple submission letter'].fillna('').astype(str)
    return(df)

def merge_ins_uoa(df1, df2):
    """Function to merge to dataframes left on df1 based on inst_id and uoa_id"""

    ## [TODO] Add some unit tests on the merge here ##
    assert all(df1['inst_id'].isin(df2['inst_id']))
    assert all(df1['uoa_id'].isin(df2['uoa_id']))
    
    return(df1.merge(df2, how='left', left_on=['inst_id', 'uoa_id'],
                     right_on=['inst_id', 'uoa_id']))

def summarize_output_data(df):
    """Placeholder summarization function"""
    return(df.groupby(['inst_id', 'uoa_id']).first().reset_index())

def merge_ref_data(raw_path):
    """ Merge all REF files with the ICS data as the spine"""
    raw_ics = pd.read_excel(os.path.join(raw_path,
                                         'raw_ics_data.xlsx'))
    [n_ics, k_ics] = raw_ics.shape
    
    # 1. First lets work on the 'results' data:
    raw_results = pd.read_excel(os.path.join(raw_path,
                                             'raw_results_data.xlsx'),
                                skiprows=6)
    [n_results, k_results] = raw_results.shape
    
    ## align columns names
    raw_results = raw_results.rename(
        columns={'Institution code (UKPRN)': 'inst_id',
                 'FTE of submitted staff': 'fte',
                 '% of eligible staff submitted': 'fte_pc'})
    
    raw_ics = raw_ics.rename(
        columns={'Institution UKPRN code': 'inst_id'})
    
    raw_results = raw_results[raw_results['inst_id'] != ' ']
    raw_ics = raw_ics.copy()[raw_ics['inst_id'] != ' ']
    
    raw_results = format_ids(raw_results)
    raw_ics = format_ids(raw_ics)
    
    ## Extract some general sets and lists
    score_types = ['4*', '3*', '2*', '1*', 'Unclassified'] # types of scores
    results_ins_ids = [int(i) for i in raw_results['inst_id'].unique()] # UKPRN in results
    # UKPRN in ics
    ics_ins_ids = [int(i) for i in raw_ics['inst_id'].unique()]
    
    check_id_overlap(results_ins_ids, ics_ins_ids)
    
    ## Merge in relevant results data into the ics dataframe
    raw_ics = merge_ins_uoa(
        raw_ics, raw_results[['inst_id', 'uoa_id', 'fte', 'fte_pc']].drop_duplicates())
    
    ## Make wide score card by institution and uoa_id
    wide_score_card = pd.pivot(
        raw_results[['inst_id', 'uoa_id', 'Profile'] + score_types],
        index=['inst_id', 'uoa_id'], columns=['Profile'], values=score_types)
    wide_score_card.columns = wide_score_card.columns.map('_'.join)
    wide_score_card = wide_score_card.reset_index()
    
    ## Merge in scores
    raw_ics = merge_ins_uoa(raw_ics, wide_score_card)

    # 2. Now lets work on the output data.
    # [TODO]: Build separate script to generate descriptives at the raw_output level
    # raw_output = pd.read_excel(os.path.join(raw_path, 'raw_outputs_data.xlsx'), skiprows=4)
    # raw_output = raw_output.rename(columns = {'Institution UKPRN code': 'inst_id'})
    # raw_output = raw_output.loc[raw_output['inst_id'] != ' ']
    # raw_output = format_ids(raw_output)
    # summ_output = summarize_output_data(raw_output)
    # raw_ics = merge_ins_uoa(raw_ics, summ_output)

    # 3. Onto the environmental data, noting that this has 3 sheets:
    # 3.1. Sheet One: Research Doctoral Degrees Awarded
    raw_env_path = os.path.join(raw_path, 'raw_environment_data.xlsx')
    raw_env_doctoral = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchDoctoralDegreesAwarded", skiprows=4)
    raw_env_doctoral = raw_env_doctoral.rename(columns={'Institution UKPRN code': 'inst_id'})
    raw_env_doctoral = format_ids(raw_env_doctoral)
    
    number_cols = [col for col in raw_env_doctoral.columns if 'Number of doctoral' in col]
    raw_env_doctoral['num_doc_degrees_total'] = raw_env_doctoral[number_cols].sum(axis=1)
    raw_ics = merge_ins_uoa(
        raw_ics, raw_env_doctoral[['inst_id', 'uoa_id', 'num_doc_degrees_total']])

    # 3.2. Sheet Two: Research income
    raw_env_income = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchIncome", skiprows=4)

    raw_env_income = raw_env_income.\
        rename(columns = {'Institution UKPRN code': 'inst_id',
                          'Average income for academic years 2013-14 to 2019-20': 'av_income',
                          'Total income for academic years 2013-14 to 2019-20': 'tot_income'})
    raw_env_income = format_ids(raw_env_income)
    
    tot_inc = raw_env_income[raw_env_income['Income source'] == 'Total income']
    
    rel_inc_cols = ['inst_id', 'uoa_id', 'av_income', 'tot_income']
    
    raw_ics = merge_ins_uoa(raw_ics, tot_inc[rel_inc_cols])

    # 3.3. Research Income In-Kind
    raw_env_income_inkind = pd.read_excel(
        raw_env_path,
        sheet_name="ResearchIncomeInKind", skiprows=4)

    raw_env_income_inkind = raw_env_income_inkind.rename(
        columns={'Institution UKPRN code': 'inst_id',
                 'Total income for academic years 2013-14 to 2019-20': 'tot_inc_kind'})
    raw_env_income_inkind = format_ids(raw_env_income_inkind)

    tot_inc_kind = raw_env_income_inkind.loc[raw_env_income_inkind['Income source']=='Total income-in-kind']
    
    rel_inc_kind_cols = ['inst_id', 'uoa_id', 'tot_inc_kind']
    
    raw_ics = merge_ins_uoa(raw_ics, tot_inc_kind[rel_inc_kind_cols])
    
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    raw_ics.to_excel(os.path.join(merged_path, 'merged_ref_data_exc_output.xlsx'))
    raw_ics.to_pickle(os.path.join(merged_path, 'merged_ref_data_exc_output.pkl'))

def main():
    raw_path = os.path.join(os.getcwd(), '..', '..', 'data', 'raw')
    data_files = [f for f in listdir(raw_path)]
    
    if ~('raw_environment_data.xlsx' in data_files):
        get_environmental_data(raw_path)
    if ~('raw_ics_data.xlsx' in data_files):
        get_impact_data(raw_path)
    if ~('raw_results_data.xlsx' in data_files):
        get_all_results(raw_path)
    if ~('raw_outputs_data.xlsx' in data_files):
        get_output_data(raw_path)
        
    merge_ref_data(raw_path)


if __name__ == "__main__":
    main()