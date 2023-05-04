#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
{Script to combine all submission level data into single analysis file}

"""

import pandas as pd
import os

def main():

    ## Set paths
    edit_path = os.path.join(os.getcwd(), '..', '..', 'data', 'edit')
    final_path = os.path.join(os.getcwd(), '..', '..', 'data', 'final')

    ## Read data
    sub = pd.read_pickle(os.path.join(edit_path, 'sub_table.pkl'))
    ics_to_sub = pd.read_pickle(os.path.join(edit_path, 'ics_to_sub_table.pkl'))

    ## Merge data
    sub_final = pd.merge(sub, ics_to_sub)

    assert sub.shape[0] == sub_final.shape[0]

    ## Write data
    sub_final.to_pickle(os.path.join(final_path, 'sub_table.pkl'))

if __name__ == "__main__":
    main()