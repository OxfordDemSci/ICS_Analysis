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
    df['uoa_id'] = df['Unit of assessment number'].astype(
        str) + df['Multiple submission letter'].fillna('').astype(str)
    return(df)

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
    raw_ics = raw_ics.merge(raw_results[['inst_id', 'uoa_id', 'fte', 'fte_pc']].drop_duplicates(),
                            how='left', left_on=['inst_id', 'uoa_id'], right_on=['inst_id', 'uoa_id'])
    
    ## Make wide score card by institution and uoa_id
    wide_score_card = pd.pivot(
        raw_results[['inst_id', 'uoa_id', 'Profile'] + score_types],
        index=['inst_id', 'uoa_id'], columns=['Profile'], values=score_types)
    wide_score_card.columns = wide_score_card.columns.map('_'.join)
    wide_score_card = wide_score_card.reset_index()
    
    ## Merge in scores
    raw_ics = raw_ics.merge(wide_score_card,
                            how='left', left_on=['inst_id', 'uoa_id'], right_on=['inst_id', 'uoa_id']
                            )

    # 2. Now lets work on the output data.
    raw_output = pd.read_excel(os.path.join(raw_path, 'raw_outputs_data.xlsx'), skiprows=4)
    raw_output = raw_output.rename(columns = {'Institution UKPRN code': 'inst_id'})
    raw_output = raw_output.loc[raw_output['inst_id'] != ' ']
    
    raw_output = format_ids(raw_output)

    raw_ics['Output Journals'] = np.nan
    raw_ics['Total REF Citations'] = np.nan
    raw_ics['Number Articles'] = np.nan
    
    code = raw_ics['inst_id'][0]
    unit = raw_ics[raw_ics['inst_id']==code]['uoa_id'].unique()[0]
    raw_output.columns
    
    result_cols = ['DOI', 'Output type', 'Title', 'ISSN', 'Month', 'Year',
                   'Number of additional authors', 'Non-English', 'Interdisciplinary',
                   'Forensic science', 'Criminology', 'Propose double weighting', 'Is reserve output',
                   'Research group','Open access status','Citations applicable','Citation count']

    for code in raw_ics['inst_id'].unique():
        for unit in raw_ics[raw_ics['inst_id']==code]['uoa_id'].unique():
            temp_df = raw_output[(raw_output['inst_id']==code) &
                                 (raw_output['uoa_id']==unit)]
            output_row = {}
            output_counter = 0
            for index, row in temp_df.iterrows():
                output_row[str(output_counter)] = {}
                output_row[str(output_counter)]['DOI'] = row['DOI']
                output_row[str(output_counter)]['Output type'] = row['Output type']
                output_row[str(output_counter)]['Title'] = row['Title']
                output_row[str(output_counter)]['ISSN'] = row['ISSN']
                output_row[str(output_counter)]['Month'] = row['Month']
                output_row[str(output_counter)]['Year'] = row['Year']
                output_row[str(output_counter)]['Number of additional authors'] = row['Number of additional authors']
                output_row[str(output_counter)]['Non-English'] = row['Non-English']
                output_row[str(output_counter)]['Interdisciplinary'] = row['Interdisciplinary']
                output_row[str(output_counter)]['Forensic science'] = row['Forensic science']
                output_row[str(output_counter)]['Criminology'] = row['Criminology']
                output_row[str(output_counter)]['Propose double weighting'] = row['Propose double weighting']
                output_row[str(output_counter)]['Is reserve output'] = row['Is reserve output']
                output_row[str(output_counter)]['Research group'] = row['Research group']
                output_row[str(output_counter)]['Open access status'] = row['Open access status']
                output_row[str(output_counter)]['Citations applicable'] = row['Citations applicable']
                output_row[str(output_counter)]['Citation count'] = row['Citation count']
                output_counter =+ 1
            raw_ics['Output Journals'] = np.where((raw_ics['inst_id']==code) &
                                                  (raw_ics['uoa_id']==unit),
                                                  output_row,
                                                  raw_ics['Output Journals'])

            raw_ics['Number Articles'] = np.where((raw_ics['inst_id']==code) &
                                                  (raw_ics['uoa_id']==unit),
                                                  len(temp_df),
                                                  raw_ics['Number Articles'])
            raw_ics['Total REF Citations'] = np.where((raw_ics['inst_id']==code) &
                                                      (raw_ics['uoa_id']==unit),
                                                      temp_df['Citation count'].sum(),
                                                      raw_ics['Total REF Citations'])

    # 3. Onto the environmental data, noting that this has 3 sheets:
    # 3.1. Sheet One: Research Doctoral Degrees Awarded
    raw_file = pd.ExcelFile(os.path.join(raw_path, 'raw_environment_data.xlsx'))
    raw_env_Doctoral = raw_file.parse("ResearchDoctoralDegreesAwarded", skiprows=4)
    number_cols = [col for col in raw_env_Doctoral.columns if 'Number of doctoral' in col]
    raw_env_Doctoral['Number Doctoral Degrees'] = raw_env_Doctoral[number_cols].sum(axis=1)
    raw_env_Doctoral['inst_id'] = raw_env_Doctoral['inst_id'].astype(str)
    raw_env_Doctoral['uoa_id'] = raw_env_Doctoral['uoa_id'].astype(str)
    raw_ics['inst_id'] = raw_ics['inst_id'].astype(str)
    raw_ics['uoa_id'] = raw_ics['uoa_id'].astype(float).astype('Int64').astype(str)
    raw_ics = pd.merge(raw_ics,
                       raw_env_Doctoral[['inst_id', 'uoa_id', 'Number Doctoral Degrees']],
                       how='left',
                       left_on = ['inst_id', 'uoa_id'],
                       right_on = ['inst_id', 'uoa_id']
                      )

    # 3.2. Sheet Two: Research income
    raw_env_Income = raw_file.parse("ResearchIncome", skiprows=4)
    raw_env_Income['inst_id'] = raw_env_Income['inst_id'].astype(str)
    raw_env_Income['uoa_id'] = raw_env_Income['uoa_id'].astype(str)
    tot_inc = raw_env_Income[raw_env_Income['Income source'] == 'Total income']
    av_inc = tot_inc[['inst_id',
                      'uoa_id',
                      'Average income for academic years 2013-14 to 2019-20'
                      ]]
    tot_tot_inc = tot_inc[['inst_id',
                           'uoa_id',
                           'Total income for academic years 2013-14 to 2019-20']]
    raw_ics = pd.merge(raw_ics,
                       av_inc[['inst_id',
                               'uoa_id',
                               'Average income for academic years 2013-14 to 2019-20'
                               ]],
                       how='left',
                       left_on=['inst_id',
                                'uoa_id'],
                       right_on=['inst_id',
                                 'uoa_id']
                       )
    raw_ics = pd.merge(raw_ics,
                       tot_tot_inc[['inst_id',
                                    'uoa_id',
                                    'Total income for academic years 2013-14 to 2019-20'
                                    ]],
                       how='left',
                       left_on=['inst_id',
                                'uoa_id'],
                       right_on=['inst_id',
                                 'uoa_id']
                       )
    # 3.3. Research Income In-Kind
    raw_env_IncomeInKind = raw_file.parse("ResearchIncomeInKind", skiprows=4)
    raw_env_IncomeInKind['inst_id'] = raw_env_IncomeInKind['inst_id'].astype(str)
    raw_env_IncomeInKind['uoa_id'] = raw_env_IncomeInKind['uoa_id'].astype(str)
    tot_inc = raw_env_IncomeInKind[raw_env_IncomeInKind['Income source']=='Total income-in-kind']
    tot_tot_inc = tot_inc[['inst_id',
                           'uoa_id',
                           'Total income for academic years 2013-14 to 2019-20']]
    tot_tot_inc = tot_tot_inc.rename({'Total income for academic years 2013-14 to 2019-20':
                                      'Total income InKind for academic years 2013-14 to 2019-20'},
                                    axis=1)
    raw_ics = pd.merge(raw_ics,
                       tot_tot_inc[['inst_id',
                                    'uoa_id',
                                    'Total income InKind for academic years 2013-14 to 2019-20'
                                   ]],
                       how='left',
                       left_on = ['inst_id',
                                  'uoa_id'],
                       right_on = ['inst_id',
                                   'uoa_id']
                      )
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    raw_ics.to_csv(os.path.join(merged_path, 'merged_ref_data.csv'))

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