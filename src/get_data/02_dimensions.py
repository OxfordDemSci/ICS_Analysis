import pandas as pd
import os
import random


def format_ids(df):
    """Format id codes for merging"""

    df = df.astype({'inst_id': 'int'})
    df['uoa_id'] = df['Unit of assessment number'].astype(int).astype(
        str) + df['Multiple submission letter'].fillna('').astype(str)
    return(df)

## PLACEHOLDER SIMULATION DATA
raw_path = os.path.join(os.getcwd(), '..', '..', 'data', 'raw')

output_data = pd.read_excel(os.path.join(raw_path, 'raw_outputs_data.xlsx'),
                            skiprows=4)

output_data = output_data.\
    rename(columns={'Institution UKPRN code': 'inst_id'})
output_data = output_data.loc[output_data['inst_id'] != ' ']
output_data = format_ids(output_data)

## Make subset containing DOI, uoa_id, and inst_id
rel_set = output_data[['DOI', 'uoa_id', 'inst_id']]
rel_set = rel_set.rename(columns={'DOI': 'doi'})
rel_set = rel_set.dropna()

rel_set['no_words_abstract'] = [random.randrange(100, 500) for
                                i in range(0, rel_set.shape[0])]
rel_set['no_authors'] = [random.randrange(1, 10) for
                         i in range(0, rel_set.shape[0])]
rel_set['no_keywords'] = [random.randrange(0, 10) for
                          i in range(0, rel_set.shape[0])]
rel_set['journal_if'] = [random.gauss(4, 3) for
                         i in range(0, rel_set.shape[0])]
rel_set['journal_if'].loc[rel_set['journal_if'] < 0] = 0.1



## Write to xlsx
rel_set.to_excel(os.path.join(raw_path,'raw_dimensions_data.xlsx'))