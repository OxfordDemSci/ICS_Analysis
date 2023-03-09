#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
{Script to split the output from `get_and_merge_ref_data.py` into two datasets, one at the department level and one at the ICS level}

"""

import pandas as pd
import os

def main():
    ## Read data
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    edit_path = os.path.join(os.getcwd(), '..', '..', 'data', 'edit')
    raw_ics = pd.read_pickle(os.path.join(merged_path, 'merged_ref_data_exc_output.pkl'))

    ## Specify column types
    outcome_vars = [i for i in raw_ics.columns if '*' in i]

    sub_level_vars = [
        'uoa_id', 'Unclassified_Environment', 'Unclassified_Impact',
        'Unclassified_Outputs', 'Unclassified_Overall', 'num_doc_degrees_total',
        'av_income', 'tot_income', 'tot_inc_kind', 'fte', 'fte_pc']

    ics_level_vars = [
        'Unit of assessment number', 'Unit of assessment name',
        'Multiple submission letter', 'Multiple submission name',
        'Joint submission', 'REF impact case study identifier', 'Title',
        'Is continued from 2014', 'Summary impact type', 'Countries',
        'Formal partners', 'Funding programmes', 'Global research identifiers',
        'Name of funders', 'Researcher ORCIDs', 'Grant funding',
        '1. Summary of the impact', '2. Underpinning research',
        '3. References to the research', '4. Details of the impact',
        '5. Sources to corroborate the impact', 'COVID-19 Statement', 'uoa_id']

    id_vars = [i for i in raw_ics.columns if i not in
            sub_level_vars + ics_level_vars + outcome_vars]

    ## One-hot encode `summary impact type`
    ics = pd.concat(
        [raw_ics, pd.get_dummies(raw_ics['Summary impact type'], prefix = 'impact_type')],
        1)
    ics['sub_id'] = ics.agg('{0[inst_id]}_{0[Main panel]}_{0[uoa_id]}'.format, axis=1)

    ## Append relevant columns
    ics_level_vars = ics_level_vars + [i for i in ics if 'impact_type_' in i]
    id_vars = id_vars + ['sub_id']

    ## Write separate files
    # ICS
    ics[id_vars + ics_level_vars].to_pickle(os.path.join(edit_path, 'ics_table.pkl'))
    ics[id_vars + ics_level_vars].to_excel(os.path.join(edit_path, 'ics_table.xlsx'))

    # Submission
    sub = ics[id_vars + sub_level_vars].groupby('sub_id').first().reset_index()

    sub[id_vars + sub_level_vars + outcome_vars].to_pickle(os.path.join(edit_path, 'sub_table.pkl'))
    sub[id_vars + sub_level_vars + outcome_vars].to_excel(os.path.join(edit_path, 'sub_table.xlsx'))
    
if __name__ == "__main__":
    main()