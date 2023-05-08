#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
This script wrangles the raw REF data into the various relevant
levels of aggregation (Output, ICS, Dep)
"""

import numpy as np
import os
import pandas as pd


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
                                             'raw_results_data.xlsx'),
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
    raw_env_path = os.path.join(raw_path, 'raw_environment_data.xlsx')
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
    raw_output = pd.read_excel(os.path.join(raw_path, 'raw_outputs_data.xlsx'), skiprows=4)
    raw_output = format_ids(raw_output)
    raw_output.to_excel(os.path.join(edit_path, 'clean_ref_output_data.xlsx'))


def main():
    ## Read data
    raw_path = os.path.join(os.getcwd(), '..', '..', 'data', 'raw')
    edit_path = os.path.join(os.getcwd(), '..', '..', 'data', 'edit')
    clean_ics_level(raw_path, edit_path)
    clean_dep_level(raw_path, edit_path)
    clean_output_level(raw_path, edit_path)
    
if __name__ == "__main__":
    main()