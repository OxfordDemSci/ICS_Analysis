from pathblib import Path
import pandas as pd

PATH_TO_ICS_TABLE = "FILL THIS IN TO ICS TABLE"
FUNDERS_IN = "FILL THIS IN TO FUNDERS TABLE"
FUNDERS_OUT = "OUTPUT"

def make_funders_lookup_table(df_ics: pd.DataFrame) -> None:
    def transform_funders(row):
        if str(row.funder) != 'nan':
            return row.funder.split(';')
        return None
    df_funders = pd.read_csv(FUNDERS_IN)
    df_funders = df_funders[['REF impact case study identifier', 'Funders[full name]']]
    df_funders.rename(columns={"REF impact case study identifier": 'ics_id', 'Funders[full name]': 'funder'}, inplace=True)
    df_funders.dropna(subset='ics_id', inplace=True)
    df_ics = df_ics[['id', 'ics_id']]
    df_ics.set_index('ics_id', inplace=True)
    df_funders.set_index('ics_id', inplace=True)
    df_join = df_funders.join(df_ics)
    df_join['funders_list'] = df_join.apply(transform_funders, axis=1)
    df_join.reset_index(inplace=True)
    df_join = df_join[['id', 'funders_list']]
    df_lookup = df_join.explode('funders_list')
    df_lookup.rename(columns={'id': 'ics_table_id', 'funders_list': 'funder'}, inplace=True)
    df_lookup['id'] = df_lookup.index.copy().astype(int)
    df_lookup.to_csv(FUNDERS_OUT, index=False)