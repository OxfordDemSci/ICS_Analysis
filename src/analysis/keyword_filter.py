import os
import json
import pandas as pd


if __name__ == "__main__":
    merged_path = os.path.join(os.getcwd(), '../..', '..', 'data', 'merged')
    keyword_out = os.path.join(os.getcwd(), '../..', '..', 'data', 'keywords')
    asset_path = os.path.join(os.getcwd(), '../..', '..', 'assets')
    df = pd.read_csv(os.path.join(merged_path, 'merged_ref_data_exc_output.csv'), index_col=0)
    with open(os.path.join(asset_path, 'keyword_dictionary.json')) as json_file:
        keyword_dict = json.load(json_file)
    df = df[(df['3*_Impact'] == '0.0') &
            (df['2*_Impact']=='0.0') &
            (df['1*_Impact'] == '0.0') &
            (df['Unclassified_Impact']=='0.0')]
    df = df[(df['Main panel'] == 'D') |
            (df['Main panel'] == 'C') |
            (df['Unit of assessment number'] == '4.0')]
    freetext = ['1. Summary of the impact',
                '2. Underpinning research',
                '3. References to the research',
                '4. Details of the impact',
                '5. Sources to corroborate the impact']
    df = df[freetext]
    df = df.apply(lambda x: x.astype(str).str.lower())
    for key, value in keyword_dict.items():
        temp_df = df[df.apply(lambda r: any([kw in r[0] for kw in value]),
                              axis=1)]
        print(f'Number ICS found for {key}: ', len(temp_df))
        temp_df.to_csv(os.path.join(keyword_out, f'{key}.csv'))