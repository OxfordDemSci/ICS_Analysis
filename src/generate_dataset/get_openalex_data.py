import re
import os
import csv
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm

def load_dict(path, filename, fields):
    df = pd.read_csv(os.path.join(path, filename),
                     index_col=0, usecols = fields)
    return df


def make_long(input_df, df_col_name, delim='\n'):
    df = pd.DataFrame(columns=['Key', df_col_name])
    counter = 0
    for index, row in input_df.iterrows():
        if row[df_col_name] is not np.nan:
            split_rows = re.split(r'\n', row[df_col_name])
            for single_val in split_rows:
                df.at[counter, 'Key'] = index
                df.at[counter, df_col_name] = single_val.strip()
                counter += 1
    return df

def get_all_openalex_dois(dois_to_query):
    print(f'We have {len(dois_to_query)} DOIs to query from OpenAlex')
    base_url = 'https://api.openalex.org/works/https://doi.org/'
    doi_filepath = os.path.join(os.getcwd(),
                                '..',
                                '..',
                                'data',
                                'openalex_returns',
                                'openalex_dois.csv')
    with open(doi_filepath, 'w', newline='') as csvfile:
        fieldnames = ['doi', 'OpenAlex_Response']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for doi in tqdm(dois_to_query):
            url = base_url + doi + \
            '?mailto=charles dot rahal at demography dot ox dot ac dot uk'
            response = requests.get(url)
            if response.status_code == 200:
                writer.writerow({'doi': doi,
                                 'OpenAlex_Response': response.json()})
            elif response.status_code == 429:
                print("Woah! you're out of API keys there!")
                break
            else:
                writer.writerow({'doi': doi,
                                 'OpenAlex_Response': np.nan})

def get_openalex_data():
    print('Getting OpenAlex Data!')
    fields = ['REF impact case study identifier',
              'DOIs_suggested',
              'Titles_suggested']
    df = load_dict(os.path.join(os.getcwd(),
                                '..', '..', 'data', 'manual', 'paper_identifiers'),
                   'underpinning_research.csv',
                   fields)
    doi_df = make_long(df, 'DOIs_suggested')
    dois_to_query = doi_df["DOIs_suggested"].tolist()
    get_all_openalex_dois(dois_to_query)
    openalex_dois = pd.read_csv(os.path.join(os.getcwd(),
                                             '..',
                                             '..',
                                             'data',
                                             'openalex_returns',
                                             'openalex_dois.csv'
                                            )
                               )
    openalex_df = pd.merge(doi_df,
                           openalex_dois,
                           how='left',
                           left_on='DOIs_suggested',
                           right_on='doi')
    openalex_df = openalex_df[openalex_df['OpenAlex_Response'].notnull()]
    openalex_df = openalex_df.drop('DOIs_suggested', axis=1)
    openalex_df = openalex_df.sort_values(by=['Key', 'doi'])
    openalex_df.to_csv(os.path.join(os.getcwd(),
                                    '..',
                                    '..',
                                    'data',
                                    'openalex_returns',
                                    'merged_openalex.csv'
                                    ),
                       index=False
                       )