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


def merge_ref_data(raw_path):
    """ Merge all REF files with the ICS data as the spine"""
    raw_ics = pd.read_excel(os.path.join(raw_path,
                                         'raw_ics_data.xlsx'))
    # 1. First lets work on the 'results' data:
    raw_results = pd.read_excel(os.path.join(raw_path,
                                             'raw_results_data.xlsx'),
                                skiprows=6)
    raw_results = raw_results[raw_results['Institution code (UKPRN)'] != ' ']
    raw_ics = raw_ics.copy()[raw_ics['Institution UKPRN code'] != ' ']
    raw_ics['FTE'] = np.nan
    raw_ics['FTE_pc'] = np.nan
    for profile in raw_results['Profile'].unique():
        for star in ['4*', '3*', '2*', '1*', 'Unclassified']:
            raw_ics[profile + '_' + star + '_pc'] = np.nan
    for code in raw_results['Institution code (UKPRN)'].unique():
        temp_df = raw_results[raw_results['Institution code (UKPRN)'] == code]
        for unit in temp_df['Unit of assessment number'].unique():
            temp_df_two = temp_df[temp_df['Unit of assessment number'] == unit]
            raw_ics['FTE'] = np.where((raw_ics['Institution UKPRN code'] == str(code)) &
                                      (raw_ics['Unit of assessment number'] == unit),
                                      temp_df_two['FTE of submitted staff'].iloc[0],
                                      raw_ics['FTE'])
            raw_ics['FTE_pc'] = np.where((raw_ics['Institution UKPRN code'] == str(code)) &
                                         (raw_ics['Unit of assessment number'] == unit),
                                         temp_df_two['% of eligible staff submitted'].iloc[0],
                                         raw_ics['FTE_pc'])
            for profile in temp_df_two['Profile'].unique():
                temp_df_three = temp_df_two[temp_df_two['Profile'] == profile]
                for star in ['4*', '3*', '2*', '1*', 'Unclassified']:
                    try:
                        raw_ics[profile + '_' + star + '_pc'] = np.where(
                            (raw_ics['Institution UKPRN code'] == str(code)) &
                            (raw_ics['Unit of assessment number'] == unit),
                            float(temp_df_three[star]),
                            raw_ics[profile + '_' + star + '_pc']
                            )
                    except (ValueError, TypeError):
                        raw_ics[profile + '_' + star + '_pc'] = np.where(
                            (raw_ics['Institution UKPRN code'] == str(code)) &
                            (raw_ics['Unit of assessment number'] == unit),
                            np.nan,
                            raw_ics[profile + '_' + star + '_pc']
                            )

                        pass

    # 2. Now lets work on the output data.
    raw_output = pd.read_excel(os.path.join(raw_path, 'raw_outputs_data.xlsx'), skiprows=4)
    raw_output[raw_output['Institution UKPRN code']!=' ']
    raw_ics['Output Journals'] = np.nan
    raw_ics['Total REF Citations'] = np.nan
    raw_ics['Number Articles'] = np.nan
    for code in raw_ics['Institution UKPRN code'].unique():
        for unit in raw_ics[raw_ics['Institution UKPRN code']==code]['Unit of assessment number'].unique():
            temp_df = raw_output[(raw_output['Institution UKPRN code']==code) &
                                 (raw_output['Unit of assessment number']==unit)]
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
            raw_ics['Output Journals'] = np.where((raw_ics['Institution UKPRN code']==code) &
                                                  (raw_ics['Unit of assessment number']==unit),
                                                  output_row,
                                                  raw_ics['Output Journals'])

            raw_ics['Number Articles'] = np.where((raw_ics['Institution UKPRN code']==code) &
                                                  (raw_ics['Unit of assessment number']==unit),
                                                  len(temp_df),
                                                  raw_ics['Number Articles'])
            raw_ics['Total REF Citations'] = np.where((raw_ics['Institution UKPRN code']==code) &
                                                      (raw_ics['Unit of assessment number']==unit),
                                                      temp_df['Citation count'].sum(),
                                                      raw_ics['Total REF Citations'])

    # 3. Onto the environmental data, noting that this has 3 sheets:
    # 3.1. Sheet One: Research Doctoral Degrees Awarded
    raw_file = pd.ExcelFile(os.path.join(raw_path, 'raw_environment_data.xlsx'))
    raw_env_Doctoral = raw_file.parse("ResearchDoctoralDegreesAwarded", skiprows=4)
    number_cols = [col for col in raw_env_Doctoral.columns if 'Number of doctoral' in col]
    raw_env_Doctoral['Number Doctoral Degrees'] = raw_env_Doctoral[number_cols].sum(axis=1)
    raw_env_Doctoral['Institution UKPRN code'] = raw_env_Doctoral['Institution UKPRN code'].astype(str)
    raw_env_Doctoral['Unit of assessment number'] = raw_env_Doctoral['Unit of assessment number'].astype(str)
    raw_ics['Institution UKPRN code'] = raw_ics['Institution UKPRN code'].astype(str)
    raw_ics['Unit of assessment number'] = raw_ics['Unit of assessment number'].astype(float).astype('Int64').astype(str)
    raw_ics = pd.merge(raw_ics,
                       raw_env_Doctoral[['Institution UKPRN code', 'Unit of assessment number', 'Number Doctoral Degrees']],
                       how='left',
                       left_on = ['Institution UKPRN code', 'Unit of assessment number'],
                       right_on = ['Institution UKPRN code', 'Unit of assessment number']
                      )

    # 3.2. Sheet Two: Research income
    raw_env_Income = raw_file.parse("ResearchIncome", skiprows=4)
    raw_env_Income['Institution UKPRN code'] = raw_env_Income['Institution UKPRN code'].astype(str)
    raw_env_Income['Unit of assessment number'] = raw_env_Income['Unit of assessment number'].astype(str)
    tot_inc = raw_env_Income[raw_env_Income['Income source'] == 'Total income']
    av_inc = tot_inc[['Institution UKPRN code',
                      'Unit of assessment number',
                      'Average income for academic years 2013-14 to 2019-20'
                      ]]
    tot_tot_inc = tot_inc[['Institution UKPRN code',
                           'Unit of assessment number',
                           'Total income for academic years 2013-14 to 2019-20']]
    raw_ics = pd.merge(raw_ics,
                       av_inc[['Institution UKPRN code',
                               'Unit of assessment number',
                               'Average income for academic years 2013-14 to 2019-20'
                               ]],
                       how='left',
                       left_on=['Institution UKPRN code',
                                'Unit of assessment number'],
                       right_on=['Institution UKPRN code',
                                 'Unit of assessment number']
                       )
    raw_ics = pd.merge(raw_ics,
                       tot_tot_inc[['Institution UKPRN code',
                                    'Unit of assessment number',
                                    'Total income for academic years 2013-14 to 2019-20'
                                    ]],
                       how='left',
                       left_on=['Institution UKPRN code',
                                'Unit of assessment number'],
                       right_on=['Institution UKPRN code',
                                 'Unit of assessment number']
                       )
    # 3.3. Research Income In-Kind
    raw_env_IncomeInKind = raw_file.parse("ResearchIncomeInKind", skiprows=4)
    raw_env_IncomeInKind['Institution UKPRN code'] = raw_env_IncomeInKind['Institution UKPRN code'].astype(str)
    raw_env_IncomeInKind['Unit of assessment number'] = raw_env_IncomeInKind['Unit of assessment number'].astype(str)
    tot_inc = raw_env_IncomeInKind[raw_env_IncomeInKind['Income source']=='Total income-in-kind']
    tot_tot_inc = tot_inc[['Institution UKPRN code',
                           'Unit of assessment number',
                           'Total income for academic years 2013-14 to 2019-20']]
    tot_tot_inc = tot_tot_inc.rename({'Total income for academic years 2013-14 to 2019-20':
                                      'Total income InKind for academic years 2013-14 to 2019-20'},
                                    axis=1)
    raw_ics = pd.merge(raw_ics,
                       tot_tot_inc[['Institution UKPRN code',
                                    'Unit of assessment number',
                                    'Total income InKind for academic years 2013-14 to 2019-20'
                                   ]],
                       how='left',
                       left_on = ['Institution UKPRN code',
                                  'Unit of assessment number'],
                       right_on = ['Institution UKPRN code',
                                   'Unit of assessment number']
                      )
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    raw_ics.to_csv(os.path.join(merged_path, 'merged_ref_data.csv'))

def main():
    raw_path = os.path.join(os.getcwd(), '..', '..', 'data', 'raw')
    get_impact_data(raw_path)
    get_environmental_data(raw_path)
    get_output_data(raw_path)
    get_all_results(raw_path)
    merge_ref_data(raw_path)


if __name__ == "__main__":
    main()