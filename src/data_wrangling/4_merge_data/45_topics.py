#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
{Script to combine all submission level data into single analysis file}

"""

import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()  # define "basedir" environment variable in ./.env file

def main():

    ## Set paths
    topic_path = os.path.join(os.getcwd(), '..', '..', '..', 'data', 'topic_outputs', 'production_model')
    raw_path = os.path.join(os.getcwd(), '..', '..', '..', 'data', 'raw')
    final_path = os.path.join(os.getcwd(), '..', '..', '..', 'data', 'final')

    ## Read data
    topics1 = pd.read_csv(os.path.join(topic_path, 'ics_data_modelling_top_5_full_text.csv'))
    topics2 = pd.read_csv(os.path.join(topic_path, 'BERT_keywords_full_text.csv'))
    raw = pd.read_excel(os.path.join(raw_path, 'raw_ics_data.xlsx'))
    ## Merge data
    final = pd.merge(raw,
                     topics1[['case_id',
                              'topic_top1',
                              'prob_top1']],
                     how='left',
                     left_on='REF impact case study identifier',
                     right_on='case_id',)
    final = pd.merge(final,
                     topics2,
                     how='left',
                     left_on='topic_top1',
                     right_on='topic_id')
    final = final.drop('topic_id', axis=1)
    #    assert sub.shape[0] == sub_final.shape[0]
    final.to_csv(os.path.join(final_path, 'raw_with_topics.csv'))

    #    sub_final.to_pickle(os.path.join(final_path, 'sub_table.pkl'))

if __name__ == "__main__":
    main()