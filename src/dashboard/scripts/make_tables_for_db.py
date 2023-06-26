from pathlib import Path
import pandas as pd
import geopandas as gpd
from typing import Union
import ast
import numpy as np

from prep_ics_table import main as main_ics


def make_countries_per_ics_lookup(ics_csv: Union[Path, str] , out_csv: Union[Path, str]):
    df_ics = pd.read_csv(ics_csv)
    df_countries = df_ics[['id', 'countries']]
    df_countries['countries'] = df_countries['countries'].apply(ast.literal_eval)
    df_countries = df_countries.explode('countries')
    df_countries.rename(columns={'id': 'ics_table_id', 'countries': 'country'}, inplace=True)
    df_countries = df_countries.dropna()
    df_countries.to_csv(out_csv, index=False)

def funders_to_list(row):
    if not str(row.funders) == '[]':
        funders = str(row.funders).replace(';', ',')
        funders = funders.replace('[', '')
        funders = funders.replace(']', '')
        funders = funders.split(',')
        if not funders[0] == 'nan':
            return funders
        else:
            return np.nan
    else:
        return row.funders

def make_funders_and_ics_to_funders_lookup_table(ics_csv: Union[Path, str], lookup_csv: Union[Path, str], funders_csv: Union[Path, str]):
    df_ics = pd.read_csv(ics_csv)
    transform_funders = lambda x: [funder.strip('[]') for funder in str(x).split(';') if not str(x) == 'nan']
    df_ics['funders_list'] = df_ics['funders'].apply(transform_funders)
    df_funders_lookup = df_ics[['id', 'funders_list']]
    df_funders_lookup = df_funders_lookup.explode('funders_list')
    df_funders_lookup = df_funders_lookup.rename(columns={'id': 'ics_table_id', 'funders_list': 'funder'})
    df_funders_lookup = df_funders_lookup.dropna()
    df_funders_lookup.to_csv(lookup_csv, index=False)
    df_funders = df_funders_lookup[['funder']]
    df_funders = df_funders.drop_duplicates()
    df_funders.to_csv(funders_csv, index=False)


def make_topic_weights_table(weights_csv: Union[Path, str], topic_weights_csv: Union[Path, str]):
    df_weights = pd.read_csv(weights_csv)
    topic_prefix = 'topic_top'
    prob_prefix = 'prob_top'
    num_columns = sum(col.startswith(topic_prefix) for col in df_weights.columns)
    df_long = pd.wide_to_long(df_weights, stubnames=[topic_prefix, prob_prefix], i='case_id',j='index ', sep='', suffix=r'\d+').reset_index()
    df_long = df_long.rename(columns={topic_prefix: 'topic', prob_prefix: 'probability'})
    df_long = df_long.sort_values(['case_id']).reset_index(drop=True)
    df_long.index.name = None
    df_long.to_csv(topic_weights_csv, index=False)




if __name__ == "__main__":
    BASE = Path(__file__).resolve().parent.joinpath('data')
    ics_csv = BASE.joinpath('ICS_DATABASE_TABLE.csv')
    ics_to_country_lookup = BASE.joinpath('ICS_TO_COUNTRY_LOOKUP_TABLE.csv')
    make_countries_per_ics_lookup(ics_csv, ics_to_country_lookup)

    funders_lookup_csv = BASE.joinpath('ICS_TO_FUNDERS_LOOKUP_TABLE.csv')
    funders_csv = BASE.joinpath('FUNDERS_TABLE.csv')
    make_funders_and_ics_to_funders_lookup_table(ics_csv, funders_lookup_csv, funders_csv)

    weights_csv = BASE.joinpath('ics_data_modelling_all_full_text.csv')
    topic_weights_csv = BASE.joinpath('TOPIC_WEIGHTS_TABLE.csv')
    make_topic_weights_table(weights_csv, topic_weights_csv)

    main_ics()

