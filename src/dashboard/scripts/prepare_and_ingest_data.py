from pathlib import Path 
import pandas as pd

from prep_ics_table import main as prep_ics_table

BASE = Path(__file__).resolve().parent
DATA = BASE.joinpath('data')

def make_ics(redo_prep_ics_table=False):
    if redo_prep_ics_table:
        prep_ics_table(BASE, DATA)
    ics_table = DATA.joinpath('enriched_ref_ics_data.csv')
    df_ics = pd.read_csv(ics_table)
    print(df_ics.head())
    


if __name__ == "__main__":
    make_ics()