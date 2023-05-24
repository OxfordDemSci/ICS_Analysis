#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
{Script to aggregate ICS level data to the submission level}

"""

import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()  # define "basedir" environment variable in ./.env file

def main():
    edit_path = os.path.join(os.getenv('basedir'), 'data', 'edit')
    ics = pd.read_pickle(os.path.join(edit_path, 'ics_table.pkl'))


    vars_to_aggregate = [i for i in ics.columns if 'impact_type' in i]
    group_id = ['sub_id']

    sub = ics[group_id + vars_to_aggregate].groupby('sub_id').mean().reset_index()

    sub.to_pickle(os.path.join(edit_path, 'ics_to_sub_table.pkl'))
    sub.to_excel(os.path.join(edit_path, 'ics_to_sub_table.xlsx'))

if __name__ == "__main__":
    main()


def summarize_output_data(df):
    """Placeholder summarization function"""
    return(df.groupby(['inst_id', 'uoa_id']).first().reset_index())
