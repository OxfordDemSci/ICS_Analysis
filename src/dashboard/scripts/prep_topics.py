import os
import pandas as pd


if __name__ == '__main__':

    # topic model name
    topic_model = 'nn3nn7'

    # ---- keywords to topics table ---- #

    # load ICS-level table with merged topic model results
    dat_ics = pd.read_excel(os.path.join('data', 'dashboard', topic_model, 'candidate_' + topic_model + '.xlsx'))

    # load topic-level table: topics.xlsx (from Google Drive)
    dat_topic = pd.read_excel(os.path.join('data', 'dashboard', topic_model, 'topics.xlsx'))

    # add keywords list from ICS-level table to topic-level table
    for i in dat_topic.index:
        topic_id = dat_topic['topic_id'][i].astype(int)
        if topic_id in dat_ics['BERT_topic']:
            keywords = dat_ics[dat_ics['BERT_topic'] == topic_id]['BERT_topic_terms'].iloc[0]
            dat_topic.at[i, 'keywords'] = keywords.replace(',', ', ')

    # save to xlsx
    dat_topic.to_excel(os.path.join('data', 'dashboard', topic_model, 'topics_keywords.xlsx'),
                       index=False)
